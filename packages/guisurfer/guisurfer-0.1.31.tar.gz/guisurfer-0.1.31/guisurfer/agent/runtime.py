import base64
import os
from cryptography.fernet import Fernet
from dataclasses import dataclass, field
from typing import List, Optional, Tuple
import uuid
import time
import json
import socket
import urllib.error
import urllib.parse
import urllib.request

from kubernetes.client import Configuration
from kubernetes.client.api import core_v1_api
from kubernetes.client.rest import ApiException
from kubernetes.stream import portforward
from google.oauth2 import service_account
from google.cloud import container_v1
from google.auth.transport.requests import Request
from kubernetes import client, config
from kubernetes.client.rest import ApiException
from agentdesk.vm import DesktopVM

from guisurfer.db.conn import WithDB
from guisurfer.db.models import AgentRuntimeRecord, SharedAgentRuntimeRecord
from guisurfer.server.models import AgentRuntimeModel
from guisurfer.server.key import SSHKeyPair
from .types import AgentType
from .base import TaskAgentInstance
from .env import (
    HUB_SERVER_ENV,
    AGENTD_ADDR_ENV,
    AGENTD_PRIVATE_SSH_KEY_ENV,
    AGENTSEA_HUB_URL_ENV,
)


@dataclass
class AgentRuntime(WithDB):
    """A runtime for agents"""

    name: str
    provider: str
    owner_id: str
    credentials: dict
    created: float = field(default_factory=lambda: time.time())
    updated: float = field(default_factory=lambda: time.time())
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    metadata: dict = field(default_factory=lambda: {})
    shared_with: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.credentials = self.encrypt_credentials(self.credentials)
        self.save()

    @classmethod
    def get_encryption_key(cls) -> str:
        return os.environ["ENCRYPTION_KEY"]

    def encrypt_credentials(self, credentials: str) -> str:
        key = self.get_encryption_key()
        fernet = Fernet(key)
        encrypted_credentials = fernet.encrypt(json.dumps(credentials).encode())
        return base64.b64encode(encrypted_credentials).decode()

    @classmethod
    def decrypt_credentials(cls, encrypted_credentials: str) -> str:
        key = cls.get_encryption_key()
        fernet = Fernet(key)
        decrypted_credentials = fernet.decrypt(base64.b64decode(encrypted_credentials))
        return json.loads(decrypted_credentials.decode())

    def to_record(self) -> AgentRuntimeRecord:
        return AgentRuntimeRecord(
            id=self.id,
            owner_id=self.owner_id,
            name=self.name,
            provider=self.provider,
            credentials=self.credentials,
            created=self.created,
            updated=self.updated,
            metadata_=json.dumps(self.metadata) if self.metadata else None,
            full_name=f"{self.owner_id}/{self.name}",
        )

    @classmethod
    def from_record(cls, record: AgentRuntimeRecord) -> "AgentRuntime":
        obj = cls.__new__(cls)
        obj.id = record.id
        obj.name = record.name
        obj.provider = record.provider
        obj.credentials = record.credentials
        obj.created = record.created
        obj.owner_id = record.owner_id
        obj.updated = record.updated
        obj.shared_with = [shared.shared_with_user_id for shared in record.shared_with]
        obj.metadata = json.loads(record.metadata_) if record.metadata_ else {}
        return obj

    def to_schema(self) -> AgentRuntimeModel:
        return AgentRuntimeModel(
            id=self.id,
            name=self.name,
            provider=self.provider,
            created=self.created,
            updated=self.updated,
            metadata=self.metadata if self.metadata else {},
            shared_with=self.shared_with,
        )

    def save(self) -> None:
        for db in self.get_db():
            # Save the AgentRuntimeRecord itself
            db.merge(self.to_record())  # Use merge to handle both insert and update
            db.commit()

            # Get existing shared records from the database
            existing_shared_records = (
                db.query(SharedAgentRuntimeRecord).filter_by(runtime_id=self.id).all()
            )
            existing_shared_user_ids = {
                record.shared_with_user_id for record in existing_shared_records
            }

            # Find which user IDs need to be added or removed
            current_shared_user_ids = set(self.shared_with)
            users_to_add = current_shared_user_ids - existing_shared_user_ids
            users_to_remove = existing_shared_user_ids - current_shared_user_ids

            # Remove records for users no longer shared with
            for user_id in users_to_remove:
                db.query(SharedAgentRuntimeRecord).filter_by(
                    runtime_id=self.id, shared_with_user_id=user_id
                ).delete()

            # Add new shared user records
            for user_id in users_to_add:
                new_shared_runtime = SharedAgentRuntimeRecord(
                    runtime_id=self.id, shared_with_user_id=user_id
                )
                db.add(new_shared_runtime)

            db.commit()

    @classmethod
    def find(cls, **kwargs) -> List["AgentRuntime"]:
        for db in cls.get_db():
            records = db.query(AgentRuntimeRecord).filter_by(**kwargs).all()
            return [cls.from_record(record) for record in records]

    @classmethod
    def delete(cls, name: str, owner_id: str) -> None:
        """Delete runtime provider"""
        for db in cls.get_db():
            record = (
                db.query(AgentRuntimeRecord)
                .filter_by(name=name, owner_id=owner_id)
                .first()
            )
            if record:
                db.delete(record)
                db.commit()

    @classmethod
    def find_for_user(
        cls, user_id: str, name: Optional[str] = None
    ) -> List["AgentRuntime"]:
        """Find runtimes owned by the user and those shared with them, optionally filtering by name."""
        runtimes = []  # Initialize the list to hold the runtime instances

        for db in cls.get_db():
            # Define the base condition for shared runtimes
            shared_conditions = [
                SharedAgentRuntimeRecord.shared_with_user_id == user_id
            ]

            # Add the name filter condition if a name is provided
            if name:
                shared_conditions.append(AgentRuntimeRecord.name == name)

            # Query for owned runtimes
            owned_query = db.query(AgentRuntimeRecord).filter_by(owner_id=user_id)
            if name:
                owned_query = owned_query.filter(AgentRuntimeRecord.name == name)
            owned_runtimes = [cls.from_record(record) for record in owned_query.all()]

            # Query for shared runtimes
            shared_query = (
                db.query(AgentRuntimeRecord)
                .join(SharedAgentRuntimeRecord)
                .filter(*shared_conditions)
            )
            shared_runtimes = [cls.from_record(record) for record in shared_query.all()]

            # Combine the lists of owned and shared runtimes for this DB session
            runtimes.extend(owned_runtimes + shared_runtimes)

        return runtimes

    def share_with_user(self, user_id: str) -> None:
        if user_id not in self.shared_with:
            self.shared_with.append(user_id)
            shared_runtime = SharedAgentRuntimeRecord(
                runtime_id=self.id, shared_with_user_id=user_id
            )
            for db in self.get_db():
                db.add(shared_runtime)
                db.commit()

    def setup_kubernetes_client(self) -> Tuple[client.CoreV1Api, str, str, str]:
        """
        Sets up and returns a configured Kubernetes client (CoreV1Api) and cluster details.

        Returns:
            Tuple containing the Kubernetes CoreV1Api client object, the Kubernetes namespace, the project ID, and the cluster name.
        """
        # Decrypt service account information
        creds = self.decrypt_credentials(self.credentials)
        service_account_json = creds.get("GOOGLE_APPLICATION_CREDENTIALS_JSON")
        if not service_account_json:
            raise ValueError(
                "GOOGLE_APPLICATION_CREDENTIALS_JSON not found in credentials"
            )

        service_account_info = json.loads(service_account_json)
        credentials = service_account.Credentials.from_service_account_info(
            service_account_info,
            scopes=["https://www.googleapis.com/auth/cloud-platform"],
        )

        # Setup GKE client to get cluster information
        gke_service = container_v1.ClusterManagerClient(credentials=credentials)
        cluster_name = self.metadata.get("CLUSTER_NAME")
        region = self.metadata.get("REGION")
        project_id = service_account_info.get("project_id")
        if not project_id or not cluster_name or not region:
            raise ValueError(
                "Missing project_id, cluster_name, or region in credentials or metadata"
            )

        print("getting cluster...")
        cluster_request = container_v1.GetClusterRequest(
            name=f"projects/{project_id}/locations/{region}/clusters/{cluster_name}"
        )
        cluster = gke_service.get_cluster(request=cluster_request)
        print("got cluster: ", cluster)

        # Configure Kubernetes client
        print("getting token...")
        ca_cert = base64.b64decode(cluster.master_auth.cluster_ca_certificate)
        credentials.refresh(Request())
        access_token = credentials.token
        print("got token: ", access_token)

        kubeconfig = {
            "apiVersion": "v1",
            "kind": "Config",
            "clusters": [
                {
                    "name": cluster_name,
                    "cluster": {
                        "server": f"https://{cluster.endpoint}",
                        "certificate-authority-data": base64.b64encode(
                            ca_cert
                        ).decode(),
                    },
                }
            ],
            "contexts": [
                {
                    "name": cluster_name,
                    "context": {
                        "cluster": cluster_name,
                        "user": cluster_name,
                    },
                }
            ],
            "current-context": cluster_name,
            "users": [
                {
                    "name": cluster_name,
                    "user": {
                        "token": access_token,
                    },
                }
            ],
        }

        config.load_kube_config_from_dict(config_dict=kubeconfig)
        v1_client = client.CoreV1Api()

        namespace = self.metadata.get("NAMESPACE", "default")

        return v1_client, namespace, project_id, cluster_name

    def delete_agent(self, name: str) -> None:
        """
        Deletes resources associated with a given agent.

        Parameters:
            name (str): The name of the agent whose resources are to be deleted.
        """
        if self.provider == "gke":
            v1, namespace, project_id, cluster_name = self.setup_kubernetes_client()
            # Delete the Pod
            try:
                v1.delete_namespaced_pod(name=name.lower(), namespace=namespace)
                print(f"Pod {name.lower()} deleted successfully.")
            except ApiException as e:
                print(f"Error deleting pod: {e}")

            # Delete the Secret
            try:
                v1.delete_namespaced_secret(name=name.lower(), namespace=namespace)
                print(f"Secret {name.lower()} deleted successfully.")
            except ApiException as e:
                print(f"Error deleting secret: {e}")
        else:
            raise ValueError("Unknown agent runtime provider")

    def status(self, name: str) -> str:
        if self.provider == "gke":
            v1, namespace, project_id, cluster_name = self.setup_kubernetes_client()
            try:
                pod: client.V1Pod = v1.read_namespaced_pod(
                    name=name, namespace=namespace
                )
                status: client.V1PodStatus = pod.status
            except ApiException as e:
                print(f"Exception when calling CoreV1Api->read_namespaced_pod: {e}")

            return status
        else:
            raise ValueError("Unknown agent runtime provider")

    def call(
        self, name: str, path: str, method: str, data: Optional[dict] = None
    ) -> dict:
        v1, namespace, project_id, cluster_name = self.setup_kubernetes_client()

        c = Configuration.get_default_copy()
        c.assert_hostname = False
        Configuration.set_default(c)
        core_v1 = core_v1_api.CoreV1Api()
        ##############################################################################
        # Kubernetes pod port forwarding works by directly providing a socket which
        # the python application uses to send and receive data on. This is in contrast
        # to the go client, which opens a local port that the go application then has
        # to open to get a socket to transmit data.
        #
        # This simplifies the python application, there is not a local port to worry
        # about if that port number is available. Nor does the python application have
        # to then deal with opening this local port. The socket used to transmit data
        # is immediately provided to the python application.
        #
        # Below also is an example of monkey patching the socket.create_connection
        # function so that DNS names of the following formats will access kubernetes
        # ports:
        #
        #    <pod-name>.<namespace>.kubernetes
        #    <pod-name>.pod.<namespace>.kubernetes
        #    <service-name>.svc.<namespace>.kubernetes
        #    <service-name>.service.<namespace>.kubernetes
        #
        # These DNS name can be used to interact with pod ports using python libraries,
        # such as urllib.request and http.client. For example:
        #
        # response = urllib.request.urlopen(
        #     'https://metrics-server.service.kube-system.kubernetes/'
        # )
        #
        ##############################################################################

        # Monkey patch socket.create_connection which is used by http.client and
        # urllib.request. The same can be done with urllib3.util.connection.create_connection
        # if the "requests" package is used.
        socket_create_connection = socket.create_connection

        def kubernetes_create_connection(address, *args, **kwargs):
            dns_name = address[0]
            if isinstance(dns_name, bytes):
                dns_name = dns_name.decode()
            dns_name = dns_name.split(".")
            if dns_name[-1] != "kubernetes":
                return socket_create_connection(address, *args, **kwargs)
            if len(dns_name) not in (3, 4):
                raise RuntimeError("Unexpected kubernetes DNS name.")
            namespace = dns_name[-2]
            name = dns_name[0]
            port = address[1]
            print("connecting to: ", namespace, name, port)
            if len(dns_name) == 4:
                if dns_name[1] in ("svc", "service"):
                    service = core_v1.read_namespaced_service(name, namespace)
                    for service_port in service.spec.ports:
                        if service_port.port == port:
                            port = service_port.target_port
                            break
                    else:
                        raise RuntimeError(f"Unable to find service port: {port}")
                    label_selector = []
                    for key, value in service.spec.selector.items():
                        label_selector.append(f"{key}={value}")
                    pods = core_v1.list_namespaced_pod(
                        namespace, label_selector=",".join(label_selector)
                    )
                    if not pods.items:
                        raise RuntimeError("Unable to find service pods.")
                    name = pods.items[0].metadata.name
                    if isinstance(port, str):
                        for container in pods.items[0].spec.containers:
                            for container_port in container.ports:
                                if container_port.name == port:
                                    port = container_port.container_port
                                    break
                            else:
                                continue
                            break
                        else:
                            raise RuntimeError(
                                f"Unable to find service port name: {port}"
                            )
                elif dns_name[1] != "pod":
                    raise RuntimeError(f"Unsupported resource type: {dns_name[1]}")
            pf = portforward(
                core_v1.connect_get_namespaced_pod_portforward,
                name,
                namespace,
                ports=str(port),
            )
            return pf.socket(port)

        socket.create_connection = kubernetes_create_connection

        namespace = self.metadata.get("NAMESPACE")
        if not namespace:
            raise ValueError("NAMESPACE environment variable not set")
        # Access the nginx http server using the
        # "<pod-name>.pod.<namespace>.kubernetes" dns name.
        # Construct the URL with the custom path
        url = f"http://{name.lower()}.pod.{namespace}.kubernetes:8000{path}"

        # Create a request object based on the HTTP method
        if method.upper() == "GET":
            if data:
                # Convert data to URL-encoded query parameters for GET requests
                query_params = urllib.parse.urlencode(data)
                url += f"?{query_params}"
            request = urllib.request.Request(url)
        else:
            # Set the request method and data for POST, PUT, etc.
            request = urllib.request.Request(url, method=method.upper())
            if data:
                # Convert data to JSON string and set the request body
                request.add_header("Content-Type", "application/json")
                request.data = json.dumps(data).encode("utf-8")
            print(f"Request Data: {request.data}")

        # Send the request and handle the response
        try:
            response = urllib.request.urlopen(request)
            status_code = response.code
            response_data = response.read().decode("utf-8")
            print(f"Status Code: {status_code}")

            # Parse the JSON response and return a dictionary
            return json.loads(response_data)
        except urllib.error.HTTPError as e:
            status_code = e.code
            error_message = e.read().decode("utf-8")
            print(f"Error: {status_code}")
            print(error_message)

            raise SystemError(
                f"Error making http request kubernetes pod {status_code}: {error_message}"
            )
        finally:
            try:
                if response:
                    response.close()
            except:
                pass

    def run(
        self,
        name: str,
        type: str,
        desktop: str,
        owner_id: str,
        envs: dict = {},
        secrets: dict = {},
        metadata: dict = {},
        wait_ready: bool = True,
        icon: Optional[str] = None,
    ) -> TaskAgentInstance:
        agent_types = AgentType.find(name=type)
        if not agent_types:
            raise ValueError(f"No agent type found with name {type}")
        agent_type = agent_types[0]

        desktop_vm = DesktopVM.get(name=desktop)
        if not desktop_vm:
            raise ValueError(f"No desktop found with name {desktop}")

        task_agents = TaskAgentInstance.find(name=name, owner_id=owner_id)
        if not task_agents:
            raise ValueError(f"Could not find task agent instance '{name}'")
        task_agent = task_agents[0]

        SERVER_ADDRESS = os.getenv("SERVER_ADDRESS")
        if not SERVER_ADDRESS:
            raise ValueError("$SERVER_ADDRESS environment variable must be set")

        if self.provider == "gke":
            print("creating gke agent...")
            v1, namespace, project_id, cluster_name = self.setup_kubernetes_client()

            # Find the SSH key for the desktop VM
            print("finding ssh key...")
            ssh_keys = SSHKeyPair.find(
                owner_id=self.owner_id, public_key=desktop_vm.ssh_key
            )
            if not ssh_keys:
                raise ValueError("No SSH key found for desktop VM")
            ssh_key = ssh_keys[0]
            secrets[AGENTD_PRIVATE_SSH_KEY_ENV] = ssh_key.decrypt_private_key(
                ssh_key.private_key
            )

            # Create K8s resources
            print("creating secret...")
            v1.create_namespaced_secret(
                body=client.V1Secret(
                    metadata=client.V1ObjectMeta(
                        name=name.lower(), namespace=namespace
                    ),
                    string_data=secrets,
                ),
                namespace=namespace,
            )

            k8s_envs = [client.V1EnvVar(name=k, value=v) for k, v in envs.items()]
            k8s_envs.append(client.V1EnvVar(name=HUB_SERVER_ENV, value=SERVER_ADDRESS))
            k8s_envs.append(
                client.V1EnvVar(name=AGENTD_ADDR_ENV, value=desktop_vm.addr),
            )
            k8s_envs.append(
                client.V1EnvVar(
                    name=AGENTSEA_HUB_URL_ENV, value=os.getenv(AGENTSEA_HUB_URL_ENV)
                ),
            )
            k8s_secret_envs = [
                client.V1EnvFromSource(
                    secret_ref=client.V1SecretEnvSource(
                        name=name.lower(), optional=False
                    )
                )
            ]
            k8s_resources = client.V1ResourceRequirements(
                requests={
                    "memory": agent_type.mem_request,
                    "cpu": agent_type.cpu_request,
                },
                limits={"memory": agent_type.mem_limit, "cpu": agent_type.cpu_limit},
            )

            # If GPU is used, adjust accordingly
            if agent_type.gpu_mem:
                if not k8s_resources.limits:
                    k8s_resources.limits = {}
                k8s_resources.limits["nvidia.com/gpu"] = agent_type.gpu_mem

            print("creating pod...")
            v1.create_namespaced_pod(
                body=client.V1Pod(
                    metadata=client.V1ObjectMeta(
                        name=name.lower(), namespace=namespace
                    ),
                    spec=client.V1PodSpec(
                        containers=[
                            client.V1Container(
                                name="agent",
                                image=agent_type.image,
                                ports=[client.V1ContainerPort(container_port=8000)],
                                env=k8s_envs,
                                env_from=k8s_secret_envs,
                                resources=k8s_resources,
                            )
                        ]
                    ),
                ),
                namespace=namespace,
            )
            print("created k8s resources")

            task_agent.status = "created"
            task_agent.save()

            # Wait for the pod to become Running
            if wait_ready:
                print("waiting for pod to become Running...")
                polling_interval = 5
                timeout = 700

                start_time = time.time()
                while True:
                    elapsed_time = time.time() - start_time
                    if elapsed_time > timeout:
                        print("Timeout waiting for pod to become Running.")
                        raise ValueError("Timeout waiting for pod to become Running.")

                    try:
                        pod: client.V1Pod = v1.read_namespaced_pod(
                            name=name.lower(), namespace=namespace
                        )
                        status: client.V1PodStatus = pod.status
                        if status.phase == "Running":
                            print("Pod is now running.")
                            break
                        else:
                            print(
                                f"Pod status: {status.phase}. Waiting for Running status..."
                            )
                    except ApiException as e:
                        print(
                            f"Exception when calling CoreV1Api->read_namespaced_pod: {e}"
                        )

                    time.sleep(polling_interval)

        else:
            raise ValueError(f"Unknown provider: {self.provider}")

        if not icon:
            icon = agent_type.icon

        task_agent.secrets = secrets
        task_agent.envs = envs
        task_agent.metadata = metadata
        task_agent.desktop = desktop_vm.name
        task_agent.status = "running"
        task_agent.save()
        return task_agent

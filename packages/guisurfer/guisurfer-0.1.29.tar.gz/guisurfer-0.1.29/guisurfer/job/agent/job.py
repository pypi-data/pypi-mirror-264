from typing import List, Dict
import os
import json
from kubernetes.client import (
    V1Job,
    V1JobSpec,
    V1PodTemplateSpec,
    V1ObjectMeta,
    V1PodSpec,
    V1Container,
    V1ContainerPort,
    V1EnvVar,
    V1EnvVarSource,
    V1SecretKeySelector,
    V1Pod,
    V1Secret,
)
from kubernetes import client, config
from kubernetes.client.exceptions import ApiException

from guisurfer.server.models import CreateAgentModel, V1UserProfile
from guisurfer.job.base import Job
from guisurfer.agent.env import HUB_API_KEY_ENV


def create_agent_job(
    model: CreateAgentModel, owner: V1UserProfile, job: Job, api_key: str
) -> V1Job:
    container_ports: List[V1ContainerPort] = [V1ContainerPort(container_port=8080)]

    model_json: str = json.dumps(model.model_dump(), default=str)
    owner_json: str = json.dumps(owner.model_dump(), default=str)

    common_name = f"c-agnt-{model.name}-{job.id}".lower()
    job.metadata["pod_name"] = common_name
    job.save()

    env_vars = gather_env_vars()
    env_vars["OWNER_JSON"] = owner_json
    env_vars[HUB_API_KEY_ENV] = api_key
    env_vars["MODEL_JSON"] = model_json

    namespace = os.getenv("NAMESPACE")
    create_secret_with_env_vars(
        secret_name=common_name,
        namespace=namespace,
        env_vars=env_vars,
    )
    env: List[V1EnvVar] = get_env_vars_from_secret(common_name)
    env.append(V1EnvVar(name="JOB_ID", value=job.id))

    container_image_uri = get_container_image_uri()
    print("container image uri: ", container_image_uri)

    container: V1Container = V1Container(
        name="guisurfer-job",
        image=container_image_uri,
        ports=container_ports,
        env=env,
        command=["poetry", "run", "python", "-m", "guisurfer.job.agent.main"],
    )

    job_labels = {
        "job_type": job.type,
        "job_id": job.id,
        "job_name": job.name,
        "app": "guisurfer-api",
    }
    template: V1PodTemplateSpec = V1PodTemplateSpec(
        metadata=V1ObjectMeta(labels=job_labels),
        spec=V1PodSpec(
            containers=[container],
            service_account_name="guisurfer-sa",
            restart_policy="Never",
        ),
    )

    job_spec: V1JobSpec = V1JobSpec(
        template=template, backoff_limit=0, ttl_seconds_after_finished=86400
    )
    v1job: V1Job = V1Job(
        api_version="batch/v1",
        kind="Job",
        metadata=V1ObjectMeta(name=common_name, labels=job_labels),
        spec=job_spec,
    )

    batch_v1 = client.BatchV1Api()
    v1job_result = batch_v1.create_namespaced_job(
        body=v1job,
        namespace=namespace,
    )

    update_secret_with_owner_reference(common_name, namespace, v1job_result)

    return v1job_result


def restart_agent_job(name: str, owner: V1UserProfile, job: Job, api_key: str) -> V1Job:
    container_ports: List[V1ContainerPort] = [V1ContainerPort(container_port=8080)]

    owner_json: str = json.dumps(owner.model_dump(), default=str)

    common_name = f"s-agnt-{name}-{job.id}".lower()
    job.metadata["pod_name"] = common_name
    job.save()

    env_vars = gather_env_vars()
    env_vars["OWNER_JSON"] = owner_json
    env_vars[HUB_API_KEY_ENV] = api_key
    env_vars["MODEL_JSON"] = json.dumps({"name": name})

    namespace = os.getenv("NAMESPACE")
    create_secret_with_env_vars(
        secret_name=common_name,
        namespace=namespace,
        env_vars=env_vars,
    )
    env: List[V1EnvVar] = get_env_vars_from_secret(common_name)
    env.append(V1EnvVar(name="JOB_ID", value=job.id))

    container_image_uri = get_container_image_uri()
    print("container image uri: ", container_image_uri)

    container: V1Container = V1Container(
        name="guisurfer-job",
        image=container_image_uri,
        ports=container_ports,
        env=env,
        command=["poetry", "run", "python", "-m", "guisurfer.job.agent.restart"],
    )

    job_labels = {
        "job_type": job.type,
        "job_id": job.id,
        "job_name": job.name,
        "app": "guisurfer-api",
    }
    template: V1PodTemplateSpec = V1PodTemplateSpec(
        metadata=V1ObjectMeta(labels=job_labels),
        spec=V1PodSpec(
            containers=[container],
            service_account_name="guisurfer-sa",
            restart_policy="Never",
        ),
    )

    job_spec: V1JobSpec = V1JobSpec(
        template=template, backoff_limit=0, ttl_seconds_after_finished=86400
    )
    v1job: V1Job = V1Job(
        api_version="batch/v1",
        kind="Job",
        metadata=V1ObjectMeta(name=common_name, labels=job_labels),
        spec=job_spec,
    )

    batch_v1 = client.BatchV1Api()
    v1job_result = batch_v1.create_namespaced_job(
        body=v1job,
        namespace=namespace,
    )

    update_secret_with_owner_reference(common_name, namespace, v1job_result)

    return v1job_result


def get_container_image_uri():
    config.load_incluster_config()
    v1 = client.CoreV1Api()
    pod_name = os.getenv("HOSTNAME")
    namespace = os.getenv("NAMESPACE")
    pod: V1Pod = v1.read_namespaced_pod(name=pod_name, namespace=namespace)
    for container in pod.spec.containers:
        if container.name == "guisurfer-api":
            return container.image

    raise SystemError("Could not find container image URI from current pod")


def create_secret_with_env_vars(
    secret_name: str, namespace: str, env_vars: Dict[str, str]
) -> V1Secret:
    config.load_incluster_config()
    api = client.CoreV1Api()

    secret = V1Secret(
        metadata=V1ObjectMeta(name=secret_name),
        type="Opaque",
        string_data=env_vars,
    )

    try:
        api_response = api.create_namespaced_secret(namespace=namespace, body=secret)
        print(f"Secret {secret_name} created in namespace {namespace}.")
    except ApiException as e:
        if e.status == 409:
            api_response = api.replace_namespaced_secret(
                name=secret_name, namespace=namespace, body=secret
            )
            print(f"Secret {secret_name} updated in namespace {namespace}.")
        else:
            raise
    return api_response


ENV_VARS = [
    "AGENTSEA_HUB_URL",
    "DB_USER",
    "DB_PASS",
    "DB_HOST",
    "DB_NAME",
    "DB_TYPE",
    "SERVER_ADDRESS",
    "ENCRYPTION_KEY",
]


def gather_env_vars() -> Dict[str, str]:
    return {var: os.getenv(var) for var in ENV_VARS if os.getenv(var) is not None}


def get_env_vars_from_secret(secret_name: str) -> List[V1EnvVar]:
    env_vars = ENV_VARS.copy()
    env_vars.append("OWNER_JSON")
    env_vars.append(HUB_API_KEY_ENV)
    env_vars.append("MODEL_JSON")

    env_var_secrets: List[V1EnvVar] = [
        V1EnvVar(
            name=env_name,
            value_from=V1EnvVarSource(
                secret_key_ref=V1SecretKeySelector(
                    name=secret_name,
                    key=env_name,
                )
            ),
        )
        for env_name in env_vars
    ]
    return env_var_secrets


def update_secret_with_owner_reference(secret_name: str, namespace: str, job: V1Job):
    config.load_incluster_config()
    api = client.CoreV1Api()

    secret = api.read_namespaced_secret(name=secret_name, namespace=namespace)

    owner_reference = client.V1OwnerReference(
        api_version=job.api_version,
        kind=job.kind,
        name=job.metadata.name,
        uid=job.metadata.uid,
        block_owner_deletion=True,
        controller=True,
    )

    secret.metadata.owner_references = [owner_reference]

    try:
        api.replace_namespaced_secret(
            name=secret_name, namespace=namespace, body=secret
        )
        print(
            f"Secret {secret_name} updated with owner reference in namespace {namespace}."
        )
    except ApiException as e:
        raise

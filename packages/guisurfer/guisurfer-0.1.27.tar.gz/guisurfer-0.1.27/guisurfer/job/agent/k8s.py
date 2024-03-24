from abc import ABC, abstractmethod
import os

from kubernetes import client, config

from guisurfer.server.models import CreateAgentModel, V1UserProfile
from guisurfer.job.base import Job, JobTypes, JobStatus, JobRuntime
from guisurfer.agent.base import TaskAgentInstance
from .job import create_agent_job, restart_agent_job
from .base import CreateAgentJob, RestartAgentJob


class CreateAgentJobK8s(CreateAgentJob):

    def __init__(self) -> None:
        config.load_incluster_config()
        self.batch_v1 = client.BatchV1Api()

    def create_agent(
        self, data: CreateAgentModel, owner: V1UserProfile, api_key: str
    ) -> None:
        task_agents = TaskAgentInstance.find(name=data.name, owner_id=owner.email)
        if not task_agents:
            raise ValueError(f"Could not find task agent instance {data.name}")
        task_agent = task_agents[0]

        namespace = os.getenv("NAMESPACE")
        job = Job(
            owner.email,
            JobTypes.CREATE_AGENT.value,
            JobStatus.PENDING.value,
            JobRuntime.K8s.value,
            data.name,
            namespace=namespace,
        )
        task_agent.create_job_id = job.id
        task_agent.save()

        job_created = create_agent_job(data, owner, job, api_key)
        if not namespace:
            raise Exception("$NAMESPACE env var is not set, you running on k8s dawg?")

        print("launched create agent job...")


class RestartAgentJobK8s(RestartAgentJob):

    def __init__(self) -> None:
        config.load_incluster_config()
        self.batch_v1 = client.BatchV1Api()

    def restart_agent(self, name: str, owner: V1UserProfile, api_key: str) -> None:
        task_agents = TaskAgentInstance.find(name=name, owner_id=owner.email)
        if not task_agents:
            raise ValueError(f"Could not find task agent instance {name}")
        task_agent = task_agents[0]

        namespace = os.getenv("NAMESPACE")
        job = Job(
            owner.email,
            JobTypes.CREATE_AGENT.value,
            JobStatus.PENDING.value,
            JobRuntime.K8s.value,
            name,
            namespace=namespace,
        )
        task_agent.create_job_id = job.id
        task_agent.save()

        job_created = restart_agent_job(name, owner, job, api_key)
        if not namespace:
            raise Exception("$NAMESPACE env var is not set, you running on k8s dawg?")

        print("launched restart agent job...")

from agentdesk import Desktop
import requests
import os
import json
import sys
import logging

from guisurfer.server.models import CreateAgentModel, V1UserProfile
from guisurfer.server.runtime import DesktopRuntime
from guisurfer.agent.runtime import AgentRuntime
from guisurfer.agent.base import TaskAgentInstance
from guisurfer.agent.env import HUB_API_KEY_ENV, AGENTSEA_HUB_URL_ENV
from guisurfer.job.base import Job, JobStatus
from guisurfer.job.log import StreamToLogger, BufferedJobLogHandler, StreamCapture


def create_agent(
    data: CreateAgentModel, owner: V1UserProfile, job_id: str, api_key: str
) -> None:
    jobs = Job.find(id=job_id, owner_id=owner.email)
    if not jobs:
        raise ValueError(f"Job {job_id} not found")
    job = jobs[0]
    job.status = JobStatus.RUNNING.value
    job.save()

    task_agents = TaskAgentInstance.find(name=data.name, owner_id=owner.email)
    if not task_agents:
        raise ValueError(f"Could not find task agent instance '{data.name}'")
    task_agent = task_agents[0]

    try:
        model_dict = data.model_dump()
        model_dict.pop("secrets")
        print(f"creating agent with model: {model_dict}")
        job.log(f"creating agent with model: {model_dict}")
        if data.desktop:
            print("finding desktop...")
            job.log("finding desktop...")
            desktop_vms = Desktop.find(name=data.desktop.lower(), owner_id=owner.email)
            if not desktop_vms:
                raise ValueError("Desktop not found")
            desktop_vm = desktop_vms[0]

        elif data.desktop_request:
            print("creating desktop...")
            job.log("creating desktop...")
            desktop_runtimes = DesktopRuntime.find_for_user(
                name=data.desktop_request.runtime, user_id=owner.email
            )
            if not desktop_runtimes:
                raise ValueError("DesktopRuntime not found")
            desktop_runtime = desktop_runtimes[0]

            desktop_vm = desktop_runtime.create(
                ssh_key_name=data.desktop_request.ssh_key_name,
                gce_opts=data.desktop_request.gce_opts,
                ec2_opts=data.desktop_request.ec2_opts,
                name=data.desktop_request.name,
                image=data.desktop_request.image,
                memory=data.desktop_request.memory,
                cpu=data.desktop_request.cpu,
                disk=data.desktop_request.disk,
                tags=data.desktop_request.tags,
                reserve_ip=data.desktop_request.reserve_ip,
                owner_id=owner.email,
            )
            print("created desktop")
            job.log("created desktop")

        else:
            raise ValueError("desktop or desktop_runtime is required")

        task_agent.desktop = desktop_vm.name
        task_agent.save()

        job.log("finding agent runtime...")
        print("finding agent runtime...")
        agent_runtimes = AgentRuntime.find(name=data.runtime, owner_id=owner.email)
        if not agent_runtimes:
            raise ValueError("AgentRuntime not found")
        agent_runtime = agent_runtimes[0]

        data.secrets[HUB_API_KEY_ENV] = api_key

        job.log("creating agent...")
        print("creating agent...")
        instance = agent_runtime.run(
            name=data.name,
            type=data.type,
            desktop=desktop_vm.name,
            owner_id=owner.email,
            envs=data.envs,
            secrets=data.secrets,
            metadata=data.metadata,
            wait_ready=data.wait_ready,
            icon=data.icon,
        )
        job.log("created agent")
        print("created agent")
        job.status = JobStatus.FINISHED.value
        job.result = instance.name
        job.save()

    except Exception as e:
        print(f"failed to create agent: {e}")
        job.status = JobStatus.FAILED.value
        job.result = str(e)
        job.save()
        raise e

    return


if __name__ == "__main__":
    job_id = os.getenv("JOB_ID")
    if not job_id:
        raise ValueError("JOB_ID env var not set")
    print(f"JOB_ID: {job_id}")

    owner_json = os.getenv("OWNER_JSON")
    if not owner_json:
        raise ValueError("OWNER_JSON env var not set")
    owner = V1UserProfile.model_validate(json.loads(owner_json))
    print(f"OWNER: {owner.model_dump_json()}")

    print("finding job...")
    jobs = Job.find(id=job_id, owner_id=owner.email)
    if not jobs:
        raise ValueError(f"Job {job_id} not found")
    job = jobs[0]
    print("found job")

    # print("setting up stream logger...")
    # logger = logging.getLogger(f"JobLogger_{job_id}")
    # logger.setLevel(logging.DEBUG)
    # logger.propagate = False
    # logger.info("Test direct logging to JobLogger 1.")

    # buffered_handler = BufferedJobLogHandler(job, flush_interval=1, buffer_size=1)
    # logger.addHandler(buffered_handler)
    # buffered_handler.setLevel(logging.DEBUG)

    # original_stdout = sys.stdout
    # sys.stdout = StreamCapture(original_stdout, logger, logging.INFO)

    # original_stderr = sys.stderr
    # sys.stderr = StreamCapture(original_stderr, logger, logging.ERROR)

    # logger.info("Test direct logging to JobLogger 2.")

    print("getting model json")
    model_json = os.getenv("MODEL_JSON")
    if not model_json:
        raise ValueError("MODEL_JSON env var not set")
    model = CreateAgentModel.model_validate(json.loads(model_json))
    print(f"MODEL: {model.model_dump_json()}")

    api_key = os.getenv(HUB_API_KEY_ENV)
    if not api_key:
        raise ValueError(f"{HUB_API_KEY_ENV} env var not set")
    print(f"API_KEY: {api_key}")

    create_agent(model, owner, job_id, api_key)

from agentdesk import Desktop
import requests
import os
import json
import sys
import logging

from agentdesk.vm import DesktopVM

from guisurfer.server.models import (
    V1UserProfile,
    GCEProviderOptions,
    EC2ProviderOptions,
)
from guisurfer.server.runtime import DesktopRuntime
from guisurfer.agent.runtime import AgentRuntime
from guisurfer.agent.base import TaskAgentInstance
from guisurfer.agent.env import HUB_API_KEY_ENV, AGENTSEA_HUB_URL_ENV
from guisurfer.job.base import Job, JobStatus
from guisurfer.job.log import StreamToLogger, BufferedJobLogHandler, StreamCapture


def restart_agent(name: str, owner: V1UserProfile, job_id: str, api_key: str) -> None:
    jobs = Job.find(id=job_id, owner_id=owner.email)
    if not jobs:
        raise ValueError(f"Job {job_id} not found")
    job = jobs[0]
    job.status = JobStatus.RUNNING.value
    job.save()

    task_agents = TaskAgentInstance.find(name=name, owner_id=owner.email)
    if not task_agents:
        raise ValueError(f"Could not find task agent instance '{name}'")
    task_agent = task_agents[0]

    job.log(f"Restarting agent '{name}'")

    try:
        if task_agent.desktop:
            print("starting desktop...")
            job.log(f"Starting desktop {task_agent.desktop}")
            desktops = DesktopVM.find(
                name=task_agent.desktop.lower(), owner_id=owner.email
            )
            if not desktops:
                raise Exception("Desktop not found")
            desktop = desktops[0]
            runtime_name = desktop.metadata["runtime_name"]
            print(f"\n!!finding runtime {runtime_name}...")
            # TODO: yuck
            desktop_runtimes = DesktopRuntime.find_for_user(
                name=runtime_name, user_id=owner.email
            )
            desktop_runtime = desktop_runtimes[0]
            print(f"\n!!found runtime, starting vm with provider {desktop.provider}...")
            try:
                if desktop.provider.type == "gce":
                    opts = GCEProviderOptions(
                        zone=desktop.metadata["zone"], region=desktop.metadata["region"]
                    )
                    desktop_runtime.start_vm(desktop.name, owner.email, gce_opts=opts)
                elif desktop.provider.type == "ec2":
                    opts = EC2ProviderOptions(region=desktop.metadata["region"])
                    desktop_runtime.start_vm(desktop.name, owner.email, ec2_opts=opts)
                else:
                    raise Exception("Provider not found")
                print("\n!!started desktop!")
            except Exception as e:
                print("\n!!error starting desktop: ", e)
                raise

            print("started desktop")
            job.log("started desktop")

        print("finding runtime")
        job.log("finding runtime")
        runtimes = AgentRuntime.find_for_user(
            name=task_agent.runtime, user_id=owner.email
        )
        if not runtimes:
            raise Exception("Runtime not found")
        runtime = runtimes[0]

        print("running agent...")
        job.log("running agent...")
        runtime.run(
            name=task_agent.name,
            type=task_agent.type,
            desktop=task_agent.desktop,
            owner_id=task_agent.owner_id,
            envs=task_agent.envs,
            secrets=task_agent.secrets,
            metadata=task_agent.metadata,
            wait_ready=True,
            icon=task_agent.icon,
            create_secret=False,
        )

        job.log("created agent")
        print("created agent")
        job.status = JobStatus.FINISHED.value
        job.result = name
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

    print("getting agent name....")
    model_json = os.getenv("MODEL_JSON")
    if not model_json:
        raise ValueError("MODEL_JSON env var not set")
    print(f"MODEL_JSON: {model_json}")
    model = json.loads(model_json)
    if "name" not in model:
        raise ValueError("MODEL_JSON env var does not contain 'name'")

    api_key = os.getenv(HUB_API_KEY_ENV)
    if not api_key:
        raise ValueError(f"{HUB_API_KEY_ENV} env var not set")
    print(f"API_KEY: {api_key}")

    try:
        restart_agent(model["name"], owner, job_id, api_key)
    except Exception as e:
        print(f"failed to restart agent: {e}")
        job.status = JobStatus.FAILED.value
        job.result = str(e)
        job.save()
        raise e

from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated, List

from agentdesk import Desktop
from agentdesk.vm import DesktopVM
from agentdesk.vm.load import load_provider

from guisurfer.server.models import (
    V1UserProfile,
    AgentModel,
    AgentsModel,
    CreateAgentModel,
    AgentTypeModel,
    AgentTypesModel,
    CreateAgentTypeModel,
    TasksModel,
    GCEProviderOptions,
    EC2ProviderOptions,
)
from guisurfer.agent.runtime import AgentRuntime
from guisurfer.auth.transport import get_current_user
from guisurfer.server.runtime import DesktopRuntime
from guisurfer.agent.base import TaskAgentInstance
from guisurfer.agent.types import AgentType
from guisurfer.agent.models import SolveTaskModel
from guisurfer.job.agent.k8s import CreateAgentJobK8s, RestartAgentJobK8s
from guisurfer.server.hub import Hub
from guisurfer.server.key import SSHKeyPair
from guisurfer.agent.task import Task

router = APIRouter()


@router.post("/v1/agents", response_model=AgentModel)
async def create_agent(
    current_user: Annotated[V1UserProfile, Depends(get_current_user)],
    data: CreateAgentModel,
):
    print("creating agent with model: ", data)
    print("validating data...")
    if data.desktop:
        desktop_vms = Desktop.find(
            name=data.desktop.lower(), owner_id=current_user.email
        )
        if not desktop_vms:
            raise HTTPException(
                status_code=404, detail=f"Desktop {data.desktop} not found"
            )

    elif data.desktop_request:
        desktop_runtimes = DesktopRuntime.find_for_user(
            name=data.desktop_request.runtime, user_id=current_user.email
        )
        if not desktop_runtimes:
            raise HTTPException(
                status_code=404,
                detail=f"DesktopRuntime {data.desktop_request.runtime} not found",
            )

    else:
        raise HTTPException(
            status_code=400, detail="desktop or desktop_runtime is required"
        )
    agent_runtimes = AgentRuntime.find_for_user(
        name=data.runtime, user_id=current_user.email
    )
    if not agent_runtimes:
        raise HTTPException(
            status_code=404, detail=f"AgentRuntime {data.runtime} not found"
        )

    agent_types = AgentType.find(name=data.type, owner_id=current_user.email)
    if not agent_types:
        raise HTTPException(status_code=404, detail=f"AgentType {data.type} not found")
    agent_type = agent_types[0]

    print("getting api key for agent...")
    hub = Hub()
    api_key = hub.get_api_key(current_user)

    print("creating agent instance...")
    instance = TaskAgentInstance(
        runtime=data.runtime,
        type=data.type,
        desktop=data.desktop,
        name=data.name,
        owner_id=current_user.email,
        icon=data.icon if data.icon else agent_type.icon,
    )
    print("Creating agent job...")
    job = CreateAgentJobK8s()
    job.create_agent(data=data, owner=current_user, api_key=api_key)
    print("started create agent job")

    instance.refresh()
    return instance.to_schema()


@router.get("/v1/agents", response_model=AgentsModel)
async def get_agents(current_user: Annotated[V1UserProfile, Depends(get_current_user)]):
    agents = TaskAgentInstance.find(owner_id=current_user.email)
    return AgentsModel(agents=[agent.to_schema() for agent in agents])


@router.get("/v1/agents/{name}", response_model=AgentModel)
async def get_agent(
    current_user: Annotated[V1UserProfile, Depends(get_current_user)], name: str
):
    agent: List[TaskAgentInstance] = TaskAgentInstance.find(
        name=name, owner_id=current_user.email
    )
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent[0].to_schema()


@router.delete("/v1/agents/{name}")
async def delete_agent(
    current_user: Annotated[V1UserProfile, Depends(get_current_user)], name: str
):
    print(f"\n!!!deleting agent {name}...")
    try:
        task_agents = TaskAgentInstance.find(name=name, owner_id=current_user.email)
        if not task_agents:
            raise HTTPException(status_code=404, detail="Agent not found")
        task_agent = task_agents[0]
        print("task_agent: ", task_agent)
        task_agent.status = "deleting"
        task_agent.save()

        runtimes = AgentRuntime.find_for_user(
            name=task_agent.runtime, user_id=current_user.email
        )
        if not runtimes:
            raise HTTPException(status_code=404, detail="AgentRuntime not found")
        runtime = runtimes[0]
        print("runtime: ", runtime)

        print("\n!!deleting running agent...")
        runtime.delete_agent(name)
        print("\n!!deleted running agent")
    except Exception as e:
        print("\n!!error deleting agent: ", e)
        raise

    if task_agent.desktop:
        print("\n!!deleting desktop...")
        desktops = DesktopVM.find(
            name=task_agent.desktop.lower(), owner_id=current_user.email
        )
        if not desktops:
            raise HTTPException(status_code=404, detail="Desktop not found")
        desktop = desktops[0]

        runtime_name = desktop.metadata["runtime_name"]
        print(f"\n!!finding runtime {runtime_name}...")
        # TODO: yuck
        desktop_runtimes = DesktopRuntime.find_for_user(
            name=runtime_name, user_id=current_user.email
        )
        desktop_runtime = desktop_runtimes[0]
        print(f"\n!!found runtime, deleting vm with provider {desktop.provider}...")
        try:
            if desktop.provider.type == "gce":
                opts = GCEProviderOptions(
                    zone=desktop.metadata["zone"], region=desktop.metadata["region"]
                )
                desktop_runtime.delete_vm(
                    desktop.name, current_user.email, gce_opts=opts
                )
            elif desktop.provider.type == "ec2":
                opts = EC2ProviderOptions(region=desktop.metadata["region"])
                desktop_runtime.delete_vm(
                    desktop.name, current_user.email, ec2_opts=opts
                )
            else:
                raise HTTPException(status_code=404, detail="Provider not found")
            print("\n!!deleted desktop!")
        except Exception as e:
            print("\n!!error deleting desktop: ", e)

        try:
            ssh_keys = SSHKeyPair.find(
                owner_id=current_user.email, public_key=desktop.ssh_key
            )
            print("\n!!ssh keys: ", ssh_keys)
            if ssh_keys:
                print("\n!!found ssh keys to delete")
                ssh_key = ssh_keys[0]
                ssh_key.delete(ssh_key.name, ssh_key.owner_id)
                print("\n!!deleted ssh key")
        except Exception as e:
            print("\n!!error deleting ssh key: ", e)
    else:
        print("\n!!no desktop to delete")

    print("\n!!deleting agent record...")
    try:
        TaskAgentInstance.delete(id=task_agent.id)
    except Exception as e:
        print("\n!!error deleting agent record: ", e)


@router.post("/v1/agents/{name}/stop")
async def stop_agent(
    current_user: Annotated[V1UserProfile, Depends(get_current_user)], name: str
):
    print("\n!stopping agent...")
    try:
        task_agents = TaskAgentInstance.find(name=name, owner_id=current_user.email)
        if not task_agents:
            raise HTTPException(status_code=404, detail="Agent not found")
        task_agent = task_agents[0]
        print("task_agent: ", task_agent)
        task_agent.status = "stopped"
        task_agent.save()

        runtimes = AgentRuntime.find_for_user(
            name=task_agent.runtime, user_id=current_user.email
        )
        if not runtimes:
            raise HTTPException(status_code=404, detail="AgentRuntime not found")
        runtime = runtimes[0]
        print("runtime: ", runtime)

        print("\n!!stop - deleting running agent...")
        runtime.delete_agent(name)
        print("\n!!stop - deleted running agent")
    except Exception as e:
        print("\n!!stop - error deleting agent: ", e)
        raise
    print("\n!stopped running agent")

    if task_agent.desktop:
        print("\n!stopping desktop...")
        desktops = DesktopVM.find(
            name=task_agent.desktop.lower(), owner_id=current_user.email
        )
        if not desktops:
            raise HTTPException(status_code=404, detail="Desktop not found")
        desktop = desktops[0]
        runtime_name = desktop.metadata["runtime_name"]
        print(f"\n!!finding runtime {runtime_name}...")
        # TODO: yuck
        desktop_runtimes = DesktopRuntime.find_for_user(
            name=runtime_name, user_id=current_user.email
        )
        desktop_runtime = desktop_runtimes[0]
        print(f"\n!!found runtime, stopping vm with provider {desktop.provider}...")
        try:
            if desktop.provider.type == "gce":
                opts = GCEProviderOptions(
                    zone=desktop.metadata["zone"], region=desktop.metadata["region"]
                )
                desktop_runtime.stop_vm(desktop.name, current_user.email, gce_opts=opts)
            elif desktop.provider.type == "ec2":
                opts = EC2ProviderOptions(region=desktop.metadata["region"])
                desktop_runtime.stop_vm(desktop.name, current_user.email, ec2_opts=opts)
            else:
                raise HTTPException(status_code=404, detail="Provider not found")
            print("\n!!stopped desktop!")
        except Exception as e:
            print("\n!!error stopping desktop: ", e)

        print("stopped desktop")


@router.post("/v1/agents/{name}/start")
async def start_agent(
    current_user: Annotated[V1UserProfile, Depends(get_current_user)], name: str
):
    print(f"restarting agent {name}...")
    task_agents = TaskAgentInstance.find(name=name, owner_id=current_user.email)
    if not task_agents:
        raise HTTPException(status_code=404, detail="Agent not found")
    task_agent = task_agents[0]
    task_agent.status == "restarting"
    task_agent.create_job_id = None
    task_agent.save()
    print("validating data...")
    if task_agent.desktop:
        desktop_vms = Desktop.find(
            name=task_agent.desktop.lower(), owner_id=current_user.email
        )
        if not desktop_vms:
            raise HTTPException(
                status_code=404, detail=f"Desktop {task_agent.desktop} not found"
            )
    else:
        raise HTTPException(status_code=400, detail="desktop is required")

    agent_runtimes = AgentRuntime.find_for_user(
        name=task_agent.runtime, user_id=current_user.email
    )
    if not agent_runtimes:
        raise HTTPException(
            status_code=404, detail=f"AgentRuntime {task_agent.runtime} not found"
        )

    print("getting api key for agent...")
    hub = Hub()
    api_key = hub.get_api_key(current_user)

    print("Creating agent job...")
    job = RestartAgentJobK8s()
    job.restart_agent(name=name, owner=current_user, api_key=api_key)
    print("started create agent job")

    task_agent.refresh()
    return task_agent.to_schema()


@router.post("/v1/agents/{name}/tasks")
async def solve_task(
    current_user: Annotated[V1UserProfile, Depends(get_current_user)],
    name: str,
    task_model: SolveTaskModel,
):
    print("finding agent...")
    task_agents = TaskAgentInstance.find(name=name, owner_id=current_user.email)
    if not task_agents:
        raise HTTPException(status_code=404, detail="Agent not found")
    task_agent = task_agents[0]

    print("finding runtime")
    runtimes = AgentRuntime.find_for_user(
        name=task_agent.runtime, user_id=current_user.email
    )
    if not runtimes:
        raise HTTPException(status_code=404, detail="Runtime not found")
    runtime = runtimes[0]

    print("finding task...")
    found_task = Task.find(id=task_model.task.id, owner_id=current_user.email)
    if not found_task:
        print("creating task...")
        task = Task.from_schema(task_model.task, current_user.email)
        task.save()
        print("created task")
    else:
        task = found_task[0]
    task.assigned_to = task_agent.name
    task.save()
    task_model.task = task.to_schema()

    print("telling agent to start task...")
    runtime.call(name, "/v1/tasks", "POST", task_model.model_dump())
    print("agent started task")

    return


@router.get("/v1/agents/{name}/tasks", response_model=TasksModel)
async def get_tasks(
    current_user: Annotated[V1UserProfile, Depends(get_current_user)],
    name: str,
):
    print("finding agent...")
    task_agents = TaskAgentInstance.find(name=name, owner_id=current_user.email)
    if not task_agents:
        raise HTTPException(status_code=404, detail="Agent not found")
    task_agent = task_agents[0]

    print("finding task...")
    found_tasks = Task.find(assigned_to=name, owner_id=current_user.email)
    if not found_tasks:
        return TasksModel(tasks=[])

    return TasksModel(tasks=[task.to_schema() for task in found_tasks])


@router.post("/v1/agenttypes", response_model=AgentTypeModel)
async def create_types(
    current_user: Annotated[V1UserProfile, Depends(get_current_user)],
    data: CreateAgentTypeModel,
):
    agent = AgentType(
        name=data.name,
        owner_id=current_user.email,
        description=data.description,
        image=data.image,
        env_opts=data.env_opts,
        supported_runtimes=data.supported_runtimes,
        public=data.public,
    )
    return agent.to_schema()


@router.get("/v1/agenttypes", response_model=AgentTypesModel)
async def get_types(current_user: Annotated[V1UserProfile, Depends(get_current_user)]):
    user_types = AgentType.find(owner_id=current_user.email)

    public_types = [
        agent
        for agent in AgentType.find(public=True)
        if agent.id not in [user_agent.id for user_agent in user_types]
    ]
    types = user_types + public_types
    return AgentTypesModel(types=[agent.to_schema() for agent in types])


@router.get("/v1/agenttypes/{name}", response_model=AgentTypeModel)
async def get_type(
    current_user: Annotated[V1UserProfile, Depends(get_current_user)], name: str
):
    agents = AgentType.find(name=name, owner_id=current_user.email)

    if not agents:
        agents = AgentType.find(name=name, public=True)
        if not agents:
            raise HTTPException(status_code=404, detail="Agent type not found")

    return agents[0].to_schema()


@router.delete("/v1/agenttypes/{name}")
async def delete_type(
    current_user: Annotated[V1UserProfile, Depends(get_current_user)], name: str
):
    AgentType.delete(name=name, owner_id=current_user.email)
    return

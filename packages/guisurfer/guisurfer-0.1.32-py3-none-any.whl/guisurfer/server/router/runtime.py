from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

from guisurfer.server.models import (
    V1UserProfile,
    DesktopRuntimeModel,
    CreateAgentRuntimeModel,
    CreateDesktopRuntimeModel,
    DesktopRuntimesModel,
    AgentRuntimeModel,
    AgentRuntimesModel,
)
from guisurfer.agent.runtime import AgentRuntime
from guisurfer.auth.transport import get_current_user
from guisurfer.server.runtime import DesktopRuntime

router = APIRouter()


@router.post("/v1/runtimes/desktops", response_model=DesktopRuntimeModel)
async def create_desktop_runtime(
    current_user: Annotated[V1UserProfile, Depends(get_current_user)],
    data: CreateDesktopRuntimeModel,
):
    print("\ncreating desktop runtime with model: ", data.model_dump())
    runtime = DesktopRuntime(
        provider=data.provider,
        credentials=data.credentials,
        name=data.name,
        owner_id=current_user.email,
        shared_with=data.shared_with,
    )
    return runtime.to_schema()


@router.get("/v1/runtimes/desktops", response_model=DesktopRuntimesModel)
async def get_desktop_runtimes(
    current_user: Annotated[V1UserProfile, Depends(get_current_user)]
):
    runtimes = DesktopRuntime.find_for_user(user_id=current_user.email)
    return DesktopRuntimesModel(runtimes=[runtime.to_schema() for runtime in runtimes])


@router.get("/v1/runtimes/desktops/{name}", response_model=DesktopRuntimeModel)
async def get_desktop_runtime(
    current_user: Annotated[V1UserProfile, Depends(get_current_user)], name: str
):
    runtime = DesktopRuntime.find_for_user(name=name, user_id=current_user.email)
    if not runtime:
        raise HTTPException(status_code=404, detail="DesktopRuntime not found")
    return runtime[0].to_schema()


@router.delete("/v1/runtimes/desktops/{name}")
async def delete_desktop_runtime(
    current_user: Annotated[V1UserProfile, Depends(get_current_user)], name: str
):
    DesktopRuntime.delete(name=name, owner_id=current_user.email)
    return {"message": "DesktopRuntime deleted successfully"}


# ---


@router.post("/v1/runtimes/agents", response_model=AgentRuntimeModel)
async def create_agent_runtime(
    current_user: Annotated[V1UserProfile, Depends(get_current_user)],
    data: CreateAgentRuntimeModel,
):
    print("\n\ncreating agent runtime: ", data.model_dump())
    runtime = AgentRuntime(
        provider=data.provider,
        credentials=data.credentials,
        name=data.name,
        owner_id=current_user.email,
        metadata=data.metadata,
        shared_with=data.shared_with,
    )
    return runtime.to_schema()


@router.get("/v1/runtimes/agents", response_model=AgentRuntimesModel)
async def get_agent_runtimes(
    current_user: Annotated[V1UserProfile, Depends(get_current_user)]
):
    runtimes = AgentRuntime.find_for_user(user_id=current_user.email)
    return AgentRuntimesModel(runtimes=[runtime.to_schema() for runtime in runtimes])


@router.get("/v1/runtimes/agents/{name}", response_model=AgentRuntimeModel)
async def get_agent_runtime(
    current_user: Annotated[V1UserProfile, Depends(get_current_user)], name: str
):
    runtime = AgentRuntime.find_for_user(name=name, user_id=current_user.email)
    if not runtime:
        raise HTTPException(status_code=404, detail="DesktopRuntime not found")
    return runtime[0].to_schema()


@router.delete("/v1/runtimes/agents/{name}")
async def delete_agent_runtime(
    current_user: Annotated[V1UserProfile, Depends(get_current_user)], name: str
):
    AgentRuntime.delete(name=name, owner_id=current_user.email)
    return {"message": "DesktopRuntime deleted successfully"}

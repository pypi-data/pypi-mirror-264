from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

import asyncssh
from agentdesk.server.models import V1Desktop, V1DesktopReqeust, V1Desktops
from agentdesk.vm import DesktopVM
from agentdesk import Desktop
from agentdesk.util import find_open_port

from guisurfer.server.models import (
    V1UserProfile,
    CreateDesktopModel,
    ActionModel,
    ActionResponseModel,
)
from guisurfer.server.key import SSHKeyPair
from guisurfer.auth.transport import get_current_user
from guisurfer.server.runtime import DesktopRuntime

router = APIRouter()


@router.post("/v1/desktops", response_model=V1Desktop)
async def create_desktop(
    current_user: Annotated[V1UserProfile, Depends(get_current_user)],
    data: CreateDesktopModel,
):
    runtimes = DesktopRuntime.find_for_user(
        user_id=current_user.email, name=data.runtime
    )
    if len(runtimes) == 0:
        raise HTTPException(status_code=404, detail=f"Runtime {data.runtime} not found")
    runtime = runtimes[0]

    vm: DesktopVM = runtime.create(
        name=data.name,
        owner_id=current_user.email,
        ssh_key_name=data.ssh_key_name,
        gce_opts=data.gce_opts,
        ec2_opts=data.ec2_opts,
        image=data.image,
        memory=data.memory,
        cpu=data.cpu,
        disk=data.disk,
        tags=data.tags,
        reserve_ip=data.reserve_ip,
    )

    return vm.to_v1_schema()


@router.get("/v1/desktops", response_model=V1Desktops)
async def get_desktops(
    current_user: Annotated[V1UserProfile, Depends(get_current_user)]
):
    desktops = Desktop.find(owner_id=current_user.email)
    return V1Desktops(desktops=[desktop.to_v1_schema() for desktop in desktops])


@router.get("/v1/desktops/{name}", response_model=V1Desktop)
async def get_desktop(
    current_user: Annotated[V1UserProfile, Depends(get_current_user)], name: str
):
    found = Desktop.find(name=name, owner_id=current_user.email)
    if not found:
        raise HTTPException(status_code=404, detail="Desktop not found")

    return found[0].to_v1_schema()


@router.delete("/v1/desktops/{name}")
async def delete_desktop(
    current_user: Annotated[V1UserProfile, Depends(get_current_user)], name: str
):
    found = Desktop.find(name=name, owner_id=current_user.email)
    if not found:
        raise HTTPException(status_code=404, detail="Desktop not found")

    found[0].delete()


@router.post("/v1/desktops/{name}/exec", response_model=V1Desktop)
async def exec_desktop(
    current_user: Annotated[V1UserProfile, Depends(get_current_user)],
    name: str,
    action: ActionModel,
):
    found_desktops = Desktop.find(owner_id=current_user.email, name=name)
    if not found_desktops:
        raise HTTPException(status_code=404, detail="Desktop not found")
    desktop_vm = found_desktops[0]

    found_keys = SSHKeyPair.find(
        owner_id=current_user.email, public_key=desktop_vm.ssh_key
    )
    if not found_keys:
        raise HTTPException(status_code=404, detail="SSH key not found")
    key_pair = found_keys[0]
    private_key = key_pair.decrypt_private_key(key_pair.private_key)

    proxy_port = find_open_port()
    remote_port = 8000

    async with asyncssh.connect(
        desktop_vm.addr,
        username="agentsea",
        client_keys=[asyncssh.import_private_key(private_key)],
        known_hosts=None,
    ) as conn:
        # Setup port forwarding from localhost:proxy_port to desktop.addr:remote_port
        await conn.forward_local_port("localhost", proxy_port, "localhost", remote_port)

        desktop = Desktop(
            agentd_url=f"http://localhost:{proxy_port}", proxy_type="custom"
        )

        found_action = desktop.find_action(action.name)
        if not found_action:
            raise HTTPException(status_code=404, detail="Action not found")

        try:
            result = desktop.use(found_action, **action.parameters)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"failed to execute action {e}")

    return ActionResponseModel(
        action=action.name, result=str(result), parameters=action.parameters
    )

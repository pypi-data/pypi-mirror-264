from fastapi import APIRouter, Depends
from typing import Annotated

from guisurfer.server.models import (
    V1UserProfile,
    SSHKeyModel,
    SSHKeysModel,
    SSHKeyCreateModel,
)
from guisurfer.server.key import SSHKeyPair
from guisurfer.auth.transport import get_current_user

router = APIRouter()


@router.post("/v1/sshkeys", response_model=SSHKeyModel)
async def create_ssh_key(
    current_user: Annotated[V1UserProfile, Depends(get_current_user)],
    data: SSHKeyCreateModel,
):
    ssh_key = SSHKeyPair(
        name=data.name,
        public_key=data.public_key,
        private_key=data.private_key,
        owner_id=current_user.email,
    )
    return ssh_key.to_schema()


@router.get("/v1/sshkeys", response_model=SSHKeysModel)
async def get_ssh_keys(
    current_user: Annotated[V1UserProfile, Depends(get_current_user)]
):
    keys = SSHKeyPair.find(owner_id=current_user.email)
    return SSHKeysModel(keys=[key.to_schema() for key in keys])


@router.delete("/v1/sshkeys/{name}")
async def delete_ssh_keys(
    current_user: Annotated[V1UserProfile, Depends(get_current_user)], name: str
):
    SSHKeyPair.delete(name=name, owner_id=current_user.email)
    return {"message": "SSH key deleted successfully"}

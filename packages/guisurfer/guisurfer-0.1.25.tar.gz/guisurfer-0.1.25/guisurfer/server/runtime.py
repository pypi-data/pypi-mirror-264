import base64
import os
from cryptography.fernet import Fernet
from dataclasses import dataclass, field
from typing import List, Optional, Dict
import uuid
import time
import json

from agentdesk.vm import DesktopVM
from agentdesk.vm.ec2 import EC2Provider
from agentdesk.vm.gce import GCEProvider

from guisurfer.db.conn import WithDB
from guisurfer.db.models import (
    DesktopRuntimeRecord,
    AgentRuntimeRecord,
    SharedDesktopRuntimeRecord,
)
from .models import (
    DesktopRuntimeModel,
    AgentRuntimeModel,
    GCEProviderOptions,
    EC2ProviderOptions,
)
from .key import SSHKeyPair


@dataclass
class DesktopRuntime(WithDB):
    """A runtime for desktop vms"""

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

    def encrypt_credentials(self, credentials: dict) -> str:
        key = self.get_encryption_key()
        fernet = Fernet(key)
        encrypted_credentials = fernet.encrypt(json.dumps(credentials).encode())
        return base64.b64encode(encrypted_credentials).decode()

    @classmethod
    def decrypt_credentials(cls, encrypted_credentials: str) -> dict:
        key = cls.get_encryption_key()
        fernet = Fernet(key)
        decrypted_credentials = fernet.decrypt(base64.b64decode(encrypted_credentials))
        return json.loads(decrypted_credentials.decode())

    def to_record(self) -> DesktopRuntimeRecord:
        metadata_ = json.dumps(self.metadata) if self.metadata else None
        return DesktopRuntimeRecord(
            id=self.id,
            owner_id=self.owner_id,
            name=self.name,
            provider=self.provider,
            credentials=self.credentials,
            created=self.created,
            updated=self.updated,
            metadata_=metadata_,
            full_name=f"{self.owner_id}/{self.name}",
        )

    @classmethod
    def from_record(cls, record: DesktopRuntimeRecord) -> "DesktopRuntime":
        obj = cls.__new__(cls)
        obj.id = record.id
        obj.name = record.name
        obj.provider = record.provider
        obj.owner_id = record.owner_id
        obj.credentials = record.credentials  # Handle encryption/decryption as needed
        obj.created = record.created
        obj.updated = record.updated
        obj.metadata = json.loads(record.metadata_) if record.metadata_ else {}

        # Populate shared_with directly from the shared records
        shared_users = [shared.shared_with_user_id for shared in record.shared_with]
        obj.shared_with = shared_users

        return obj

    def to_schema(self) -> DesktopRuntimeModel:
        return DesktopRuntimeModel(
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
            # Save the DesktopRuntimeRecord itself
            db.add(self.to_record())
            db.commit()

            # Get existing shared records from the database
            existing_shared_records = (
                db.query(SharedDesktopRuntimeRecord).filter_by(runtime_id=self.id).all()
            )
            print("\nexisting shared records: ", existing_shared_records)
            existing_shared_user_ids = {
                record.shared_with_user_id for record in existing_shared_records
            }
            print("\nexising shared user ids: ", existing_shared_user_ids)

            # Find which user IDs need to be added or removed
            current_shared_user_ids = set(self.shared_with)
            print("\ncurrent shared user ids: ", current_shared_user_ids)
            users_to_add = current_shared_user_ids - existing_shared_user_ids
            print("\nusers to add: ", users_to_add)
            users_to_remove = existing_shared_user_ids - current_shared_user_ids
            print("\nusers to remove: ", users_to_remove)

            # Remove records for users no longer shared with
            for user_id in users_to_remove:
                db.query(SharedDesktopRuntimeRecord).filter_by(
                    runtime_id=self.id, shared_with_user_id=user_id
                ).delete()

            # Add new shared user records
            for user_id in users_to_add:
                new_shared_runtime = SharedDesktopRuntimeRecord(
                    runtime_id=self.id, shared_with_user_id=user_id
                )
                db.add(new_shared_runtime)

            db.commit()

    @classmethod
    def find(cls, **kwargs) -> List["DesktopRuntime"]:
        """Find a provider"""
        for db in cls.get_db():
            records = db.query(DesktopRuntimeRecord).filter_by(**kwargs).all()
            return [cls.from_record(record) for record in records]

    @classmethod
    def delete(cls, name: str, owner_id: str) -> None:
        """Delete a provider"""
        for db in cls.get_db():
            record = (
                db.query(DesktopRuntimeRecord)
                .filter_by(name=name, owner_id=owner_id)
                .first()
            )
            if record:
                db.delete(record)
                db.commit()

    def share_with_user(self, user_id: str) -> None:
        """Share the runtime with another user."""
        if user_id not in self.shared_with:
            self.shared_with.append(user_id)
            shared_runtime = SharedDesktopRuntimeRecord(
                runtime_id=self.id, shared_with_user_id=user_id
            )
            for db in self.get_db():
                db.add(shared_runtime)
                db.commit()

    @classmethod
    def find_for_user(
        cls, user_id: str, name: Optional[str] = None
    ) -> List["DesktopRuntime"]:
        """Find runtimes owned by the user and those shared with them, optionally filtering by name."""
        query_conditions = [SharedDesktopRuntimeRecord.shared_with_user_id == user_id]
        if name:
            query_conditions.append(DesktopRuntimeRecord.name == name)

        for db in cls.get_db():
            # Find owned runtimes, optionally filtered by name
            owned_query = db.query(DesktopRuntimeRecord).filter_by(owner_id=user_id)
            if name:
                owned_query = owned_query.filter(DesktopRuntimeRecord.name == name)
            owned_records = owned_query.all()
            owned_runtimes = [cls.from_record(record) for record in owned_records]

            # Find shared runtimes, optionally filtered by name
            shared_query = (
                db.query(DesktopRuntimeRecord)
                .join(SharedDesktopRuntimeRecord)
                .filter(*query_conditions)
            )
            shared_records = shared_query.all()
            shared_runtimes = [cls.from_record(record) for record in shared_records]

            return owned_runtimes + shared_runtimes

    def create(
        self,
        ssh_key_name: Optional[str] = None,
        gce_opts: Optional[GCEProviderOptions] = None,
        ec2_opts: Optional[EC2ProviderOptions] = None,
        name: Optional[str] = None,
        image: Optional[str] = None,
        memory: int = 4,
        cpu: int = 2,
        disk: str = "30gb",
        tags: Optional[Dict[str, str]] = None,
        reserve_ip: bool = False,
        owner_id: Optional[str] = None,
    ) -> DesktopVM:
        """Create a VM"""
        creds = self.decrypt_credentials(self.credentials)
        if self.provider == "gce":
            if not image:
                image = "agentd-ubuntu-22-04-20240321084622"
                print("\nset image to: ", image)
            if not gce_opts:
                raise ValueError("GCE options required")

            key = creds["GOOGLE_APPLICATION_CREDENTIALS_JSON"]
            service_account_info = json.loads(key)
            project_id = service_account_info.get("project_id")
            if not project_id:
                raise ValueError("project_id not found in credentials")
            provider = GCEProvider(
                project_id=project_id,
                zone=gce_opts.zone,
                region=gce_opts.region,
                gcp_credentials_json=key,
            )
            metadata = gce_opts.model_dump()

        elif self.provider == "ec2":
            image = None
            if not ec2_opts:
                raise ValueError("EC2 options required")

            provider = EC2Provider(
                region=ec2_opts.region,
                aws_access_key_id=creds["AWS_ACCESS_KEY_ID"],
                aws_secret_access_key=creds["AWS_SECRET_ACCESS_KEY"],
            )
            metadata = ec2_opts.model_dump()

        else:
            raise ValueError("Invalid provider")

        if ssh_key_name:
            print("finding ssh key pair")
            keys = SSHKeyPair.find(name=ssh_key_name, owner_id=owner_id)
            if not keys:
                raise ValueError("SSH key not found")
            key = keys[0]

        else:
            keys = SSHKeyPair.find(name=name, owner_id=owner_id)
            if not keys:
                print("generating ssh key pair")
                key = SSHKeyPair.generate_key(
                    name=name, owner_id=owner_id, metadata={"generated_for": name}
                )
            else:
                print("using existing ssh key pair for vm")
                key = keys[0]
                if key.metadata.get("generated_for") != name:
                    # TODO: this is funny
                    raise ValueError(
                        f"SSH key found with name '{name}' but is not tied to this desktop"
                    )

        print("\ncreating vm with keys:")
        print("\nprivate key: \n", key.decrypt_private_key(key.private_key))
        print("\npublic key: \n", key.public_key)

        metadata["runtime_id"] = self.id
        metadata["runtime_name"] = self.name
        vm = provider.create(
            name=name.lower(),
            memory=memory,
            image=image,
            cpu=cpu,
            disk=disk,
            tags=tags,
            reserve_ip=reserve_ip,
            public_ssh_key=key.public_key,
            private_ssh_key=key.decrypt_private_key(key.private_key),
            owner_id=owner_id,
            metadata=metadata,
        )

        print("\npast provider create")

        return vm

    def delete_vm(
        self,
        name: str,
        owner_id: str,
        gce_opts: Optional[GCEProviderOptions] = None,
        ec2_opts: Optional[EC2ProviderOptions] = None,
    ) -> None:
        """Delete a vm"""
        vms = DesktopVM.find(name=name, owner_id=owner_id)
        if not vms:
            raise ValueError("VM not found")

        print("found vm to delete: ", vms[0].__dict__)

        creds = self.decrypt_credentials(self.credentials)
        if self.provider == "gce":
            if not gce_opts:
                raise ValueError("GCE options required")

            key = creds["GOOGLE_APPLICATION_CREDENTIALS_JSON"]
            service_account_info = json.loads(key)
            project_id = service_account_info.get("project_id")
            if not project_id:
                raise ValueError("project_id not found in credentials")
            provider = GCEProvider(
                project_id=project_id,
                zone=gce_opts.zone,
                region=gce_opts.region,
                gcp_credentials_json=key,
            )

        elif self.provider == "ec2":
            if not ec2_opts:
                raise ValueError("EC2 options required")

            provider = EC2Provider(
                region=ec2_opts.region,
                aws_access_key_id=creds["AWS_ACCESS_KEY_ID"],
                aws_secret_access_key=creds["AWS_SECRET_ACCESS_KEY"],
            )

        print("deleting vm")
        provider.delete(name=name)
        print("deleted vm")

    def stop_vm(
        self,
        name: str,
        owner_id: str,
        gce_opts: Optional[GCEProviderOptions] = None,
        ec2_opts: Optional[EC2ProviderOptions] = None,
    ) -> None:
        """Stop a vm"""
        vms = DesktopVM.find(name=name, owner_id=owner_id)
        if not vms:
            raise ValueError("VM not found")

        print("found vm to stop: ", vms[0].__dict__)

        creds = self.decrypt_credentials(self.credentials)
        if self.provider == "gce":
            if not gce_opts:
                raise ValueError("GCE options required")

            key = creds["GOOGLE_APPLICATION_CREDENTIALS_JSON"]
            service_account_info = json.loads(key)
            project_id = service_account_info.get("project_id")
            if not project_id:
                raise ValueError("project_id not found in credentials")
            provider = GCEProvider(
                project_id=project_id,
                zone=gce_opts.zone,
                region=gce_opts.region,
                gcp_credentials_json=key,
            )

        elif self.provider == "ec2":
            if not ec2_opts:
                raise ValueError("EC2 options required")

            provider = EC2Provider(
                region=ec2_opts.region,
                aws_access_key_id=creds["AWS_ACCESS_KEY_ID"],
                aws_secret_access_key=creds["AWS_SECRET_ACCESS_KEY"],
            )

        print("stopping vm")
        provider.stop(name=name)
        print("stopped vm")

    def start_vm(
        self,
        name: str,
        owner_id: str,
        gce_opts: Optional[GCEProviderOptions] = None,
        ec2_opts: Optional[EC2ProviderOptions] = None,
    ) -> None:
        """Start a vm"""
        vms = DesktopVM.find(name=name, owner_id=owner_id)
        if not vms:
            raise ValueError("VM not found")

        print("found vm to start: ", vms[0].__dict__)

        creds = self.decrypt_credentials(self.credentials)
        if self.provider == "gce":
            if not gce_opts:
                raise ValueError("GCE options required")

            key = creds["GOOGLE_APPLICATION_CREDENTIALS_JSON"]
            service_account_info = json.loads(key)
            project_id = service_account_info.get("project_id")
            if not project_id:
                raise ValueError("project_id not found in credentials")
            provider = GCEProvider(
                project_id=project_id,
                zone=gce_opts.zone,
                region=gce_opts.region,
                gcp_credentials_json=key,
            )

        elif self.provider == "ec2":
            if not ec2_opts:
                raise ValueError("EC2 options required")

            provider = EC2Provider(
                region=ec2_opts.region,
                aws_access_key_id=creds["AWS_ACCESS_KEY_ID"],
                aws_secret_access_key=creds["AWS_SECRET_ACCESS_KEY"],
            )

        print("starting vm")
        provider.start(name=name)
        print("started vm")

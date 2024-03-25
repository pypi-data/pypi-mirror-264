from dataclasses import dataclass, field
from abc import abstractmethod, ABC
from typing import Dict, List, Optional
import uuid
import time
import json
import base64
import os
from cryptography.fernet import Fernet

from agentdesk import Desktop
from namesgenerator import get_random_name

from .task import Task
from guisurfer.db.models import AgentRecord
from guisurfer.db.conn import WithDB
from guisurfer.server.models import AgentModel


class TaskAgent(ABC):
    """An agent that works on tasks"""

    @abstractmethod
    def solve_task(
        self,
        task: Task,
        desktop: Desktop,
        max_steps: int = 10,
    ) -> Task:
        """Solve a desktop GUI task

        Args:
            task (Task): The task
            max_steps (int, optional): Max steps allowed. Defaults to 10.
            site_url (Optional[str], optional): A starting site. Defaults to None.

        Returns:
            Task: A task
        """
        pass


@dataclass
class TaskAgentInstance(WithDB):
    """An instance of a task agent"""

    runtime: str
    type: str
    desktop: Optional[str] = None
    name: str = get_random_name("-")
    owner_id: Optional[str] = None
    status: str = "defined"
    create_job_id: Optional[str] = None
    created: float = field(default_factory=lambda: time.time())
    updated: float = field(default_factory=lambda: time.time())
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    metadata: Dict[str, str] = field(default_factory=lambda: {})
    secrets: Dict[str, str] = field(default=None, init=False)
    envs: Dict[str, str] = field(default_factory=lambda: {})
    icon: Optional[str] = None

    def __post_init__(self):
        if self.secrets is not None:
            self.secrets = self.encrypt_secrets(self.secrets)
        self.save()

    @staticmethod
    def get_encryption_key() -> bytes:
        return os.environ["ENCRYPTION_KEY"].encode()

    def encrypt_secrets(self, secrets: Dict[str, str]) -> str:
        key = self.get_encryption_key()
        fernet = Fernet(key)
        encrypted_secrets = fernet.encrypt(json.dumps(secrets).encode())
        return base64.b64encode(encrypted_secrets).decode()

    @staticmethod
    def decrypt_secrets(encrypted_secrets: str) -> Dict[str, str]:
        key = TaskAgentInstance.get_encryption_key()
        fernet = Fernet(key)
        decrypted_secrets = fernet.decrypt(base64.b64decode(encrypted_secrets))
        return json.loads(decrypted_secrets.decode())

    def to_record(self) -> AgentRecord:
        encrypted_secrets = (
            self.encrypt_secrets(self.metadata) if self.metadata else None
        )
        return AgentRecord(
            id=self.id,
            name=self.name,
            type=self.type,
            runtime=self.runtime,
            owner_id=self.owner_id,
            created=self.created,
            updated=self.updated,
            desktop=self.desktop,
            status=self.status,
            create_job_id=self.create_job_id,
            metadata_=json.dumps(self.metadata),
            secrets=encrypted_secrets,
            envs=json.dumps(self.envs) if self.envs else None,
            icon=self.icon,
            full_name=f"{self.owner_id}/{self.name}",
        )

    @classmethod
    def from_record(cls, record: AgentRecord) -> "TaskAgentInstance":
        """Adjust to handle encrypted secrets"""
        obj = cls.__new__(cls)
        obj.id = record.id
        obj.name = record.name
        obj.type = record.type
        obj.runtime = record.runtime
        obj.status = record.status
        obj.desktop = record.desktop
        obj.created = record.created
        obj.updated = record.updated
        obj.status = record.status
        obj.owner_id = record.owner_id
        obj.create_job_id = record.create_job_id
        obj.metadata = json.loads(record.metadata_) if record.metadata_ else {}
        obj.envs = json.loads(record.envs) if record.envs else {}
        obj.secrets = cls.decrypt_secrets(record.secrets) if record.secrets else {}
        obj.icon = record.icon
        return obj

    def to_schema(self) -> AgentModel:
        """Converts the agent instance to a schema object."""
        return AgentModel(
            id=self.id,
            name=self.name,
            type=self.type,
            desktop=self.desktop,
            status=self.status,
            runtime=self.runtime,
            create_job_id=self.create_job_id,
            created=self.created,
            updated=self.updated,
            metadata=self.metadata,
            envs=self.envs,
            icon=self.icon,
        )

    @classmethod
    def from_schema(cls, schema: AgentModel) -> "TaskAgentInstance":
        """Creates an agent instance from a schema object."""
        return cls(
            id=schema.id,
            name=schema.name,
            type=schema.type,
            desktop=schema.desktop,
            runtime=schema.runtime,
            status=schema.status,
            created=schema.created,
            updated=schema.updated,
            metadata=schema.metadata,
            create_job_id=schema.create_job_id,
            envs=schema.envs,
            icon=schema.icon,
        )

    def save(self) -> None:
        """Saves the agent instance to the database."""
        for db in self.get_db():
            db.merge(self.to_record())
            db.commit()

    @classmethod
    def find(cls, **kwargs) -> List["TaskAgentInstance"]:
        """Finds agent instances based on given criteria."""
        for db in cls.get_db():
            records = db.query(AgentRecord).filter_by(**kwargs).all()
            return [cls.from_record(record) for record in records]

    @classmethod
    def delete(cls, id: str) -> None:
        """Deletes an agent instance based on the ID."""
        for db in cls.get_db():
            record = db.query(AgentRecord).filter_by(id=id).first()
            if record:
                db.delete(record)
                db.commit()

    def refresh(self) -> None:
        """Refreshes the instance by reloading data from the database."""
        for db in self.get_db():
            record = db.query(AgentRecord).filter_by(id=self.id).first()
            if record:
                self.runtime = record.runtime
                self.type = record.type
                self.desktop = record.desktop
                self.name = record.name
                self.owner_id = record.owner_id
                self.status = record.status
                self.create_job_id = record.create_job_id
                self.created = record.created
                self.updated = record.updated
                self.metadata = json.loads(record.metadata_) if record.metadata_ else {}
                self.secrets = (
                    self.decrypt_secrets(record.secrets) if record.secrets else {}
                )
                self.envs = json.loads(record.envs) if record.envs else {}
                self.icon = record.icon

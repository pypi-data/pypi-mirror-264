from typing import List, Optional
import uuid
import time
import json

from guisurfer.db.models import AgentTypeRecord
from guisurfer.db.conn import WithDB
from guisurfer.server.models import EnvVarOptModel, AgentTypeModel
from guisurfer.auth.default import COMMON_USER


class AgentType(WithDB):
    """A type of agent"""

    def __init__(
        self,
        name: str,
        description: str,
        image: str,
        supported_runtimes: List[str],
        owner_id: Optional[str] = None,
        env_opts: List[EnvVarOptModel] = [],
        public: bool = False,
        icon: Optional[str] = None,
        mem_request: Optional[str] = "500m",
        mem_limit: Optional[str] = "2gi",
        cpu_request: Optional[str] = "1",
        cpu_limit: Optional[str] = "4",
        gpu_mem: Optional[str] = None,
    ):
        self.id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.image = image
        self.supported_runtimes = supported_runtimes
        self.owner_id = owner_id
        self.env_opts = env_opts
        self.public = public
        self.icon = icon
        self.mem_request = mem_request
        self.mem_limit = mem_limit
        self.cpu_request = cpu_request
        self.cpu_limit = cpu_limit
        self.gpu_mem = gpu_mem
        self.created = time.time()
        self.updated = time.time()
        self.save()

    def to_schema(self) -> AgentTypeModel:
        return AgentTypeModel(
            id=self.id,
            name=self.name,
            description=self.description,
            image=self.image,
            env_opts=self.env_opts,
            supported_runtimes=self.supported_runtimes,
            created=self.created,
            updated=self.updated,
            public=self.public,
            icon=self.icon,
            mem_request=self.mem_request,
            mem_limit=self.mem_limit,
            cpu_request=self.cpu_request,
            cpu_limit=self.cpu_limit,
            gpu_mem=self.gpu_mem,
        )

    @classmethod
    def from_schema(cls, schema: AgentTypeModel) -> "AgentType":
        obj = cls.__new__(cls)
        obj.id = schema.id
        obj.name = schema.name
        obj.description = schema.description
        obj.image = schema.image
        obj.env_opts = schema.env_opts
        obj.supported_runtimes = schema.supported_runtimes
        obj.created = schema.created
        obj.updated = schema.updated
        obj.public = schema.public
        obj.icon = schema.icon
        obj.mem_limit = schema.mem_limit
        obj.mem_request = schema.mem_request
        obj.cpu_limit = schema.cpu_limit
        obj.cpu_request = schema.cpu_request
        obj.gpu_mem = schema.gpu_mem
        return obj

    def to_record(self) -> AgentTypeRecord:
        return AgentTypeRecord(
            id=self.id,
            name=self.name,
            description=self.description,
            image=self.image,
            env_opts=json.dumps([opt.model_dump() for opt in self.env_opts]),
            supported_runtimes=json.dumps(self.supported_runtimes),
            created=self.created,
            updated=self.updated,
            owner_id=self.owner_id,
            public=self.public,
            icon=self.icon,
            mem_limit=self.mem_limit,
            mem_request=self.mem_request,
            cpu_limit=self.cpu_limit,
            cpu_request=self.cpu_request,
            gpu_mem=self.gpu_mem,
        )

    @classmethod
    def from_record(cls, record: AgentTypeRecord) -> "AgentType":
        obj = cls.__new__(cls)
        obj.id = record.id
        obj.name = record.name
        obj.description = record.description
        obj.image = record.image
        obj.env_opts = [EnvVarOptModel(**opt) for opt in json.loads(record.env_opts)]
        obj.supported_runtimes = json.loads(record.supported_runtimes)
        obj.created = record.created
        obj.updated = record.updated
        obj.owner_id = record.owner_id
        obj.public = record.public
        obj.icon = record.icon
        obj.mem_limit = record.mem_limit
        obj.mem_request = record.mem_request
        obj.cpu_limit = record.cpu_limit
        obj.cpu_request = record.cpu_request
        obj.gpu_mem = record.gpu_mem
        return obj

    def save(self) -> None:
        for session in self.get_db():
            if session:
                record = self.to_record()
                session.merge(record)
                session.commit()

    @classmethod
    def find(cls, **kwargs) -> List["AgentType"]:
        for session in cls.get_db():
            if session:
                records = session.query(AgentTypeRecord).filter_by(**kwargs).all()
                return [cls.from_record(record) for record in records]

    @classmethod
    def delete(cls, id: str, owner_id: str) -> None:
        for session in cls.get_db():
            if session:
                record = (
                    session.query(AgentTypeRecord)
                    .filter_by(id=id, owner_id=owner_id)
                    .first()
                )
                if record:
                    session.delete(record)
                    session.commit()

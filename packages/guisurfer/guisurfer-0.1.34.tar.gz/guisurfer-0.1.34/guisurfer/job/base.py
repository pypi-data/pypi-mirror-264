from typing import Optional, Dict, List
import uuid
import time
import json
from enum import Enum
from dataclasses import dataclass, field, asdict

from guisurfer.db.models import JobRecord
from guisurfer.db.conn import WithDB
from guisurfer.server.models import JobModel


class JobTypes(Enum):
    CREATE_AGENT = "create-agent"
    RESTART_AGENT = "restart-agent"


class JobStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    FINISHED = "finished"
    FAILED = "failed"


class JobRuntime(Enum):
    K8s = "k8s"


@dataclass
class Job(WithDB):
    """A backgound job"""

    owner_id: str
    type: str
    status: str
    runtime: str
    name: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    namespace: Optional[str] = None
    logs: Optional[str] = None
    result: Optional[str] = None
    created: float = field(default_factory=lambda: time.time())
    updated: float = field(default_factory=lambda: time.time())
    finished: float = field(default_factory=lambda: 0.0)
    metadata: Dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.save()

    def to_record(self) -> JobRecord:
        metadata_serialized = json.dumps(self.metadata)
        return JobRecord(
            id=self.id,
            owner_id=self.owner_id,
            type=self.type,
            status=self.status,
            name=self.name,
            runtime=self.runtime,
            namespace=self.namespace,
            logs=self.logs,
            result=self.result,
            created=self.created,
            updated=self.updated,
            finished=self.finished,
            metadata_=metadata_serialized,
        )

    @classmethod
    def from_record(cls, record: JobRecord) -> "Job":
        obj = cls.__new__(cls)
        obj.id = record.id
        obj.owner_id = record.owner_id
        obj.type = record.type
        obj.name = record.name
        obj.status = record.status
        obj.runtime = record.runtime
        obj.namespace = record.namespace
        obj.logs = record.logs
        obj.result = record.result
        obj.created = record.created
        obj.updated = record.updated
        obj.finished = record.finished
        obj.metadata = json.loads(record.metadata_) if record.metadata_ else {}
        return obj

    def to_schema(self) -> "JobModel":
        return JobModel(**asdict(self))

    @classmethod
    def from_schema(cls, schema: "JobModel") -> "Job":
        obj = cls.__new__(cls)
        obj.id = schema.id
        obj.owner_id = schema.owner_id
        obj.type = schema.type
        obj.name = schema.name
        obj.status = schema.status
        obj.runtime = schema.runtime
        obj.namespace = schema.namespace
        obj.logs = schema.logs
        obj.result = schema.result
        obj.created = schema.created
        obj.updated = schema.updated
        obj.finished = schema.finished
        obj.metadata = schema.metadata
        return obj

    def log(self, message: str, add_timestamp=True) -> None:
        """Appends a log message to the job's logs, with an optional timestamp."""
        if add_timestamp:
            timestamp = time.strftime("[%Y-%m-%d %H:%M:%S]", time.gmtime())
            log_entry = f"{timestamp} {message}\n"
        else:
            log_entry = message + "\n"  # Assuming message is already formatted

        if not self.logs:
            self.logs = log_entry
        else:
            self.logs += log_entry

        self.updated = time.time()
        self.save()

    def save(self) -> None:
        for db in self.get_db():
            db.merge(self.to_record())
            db.commit()

    @classmethod
    def find(cls, **kwargs) -> List["Job"]:
        for db in cls.get_db():
            records = db.query(JobRecord).filter_by(**kwargs).all()
            return [cls.from_record(record) for record in records]

    @classmethod
    def delete(cls, id: str) -> None:
        for db in cls.get_db():
            record = db.query(JobRecord).filter_by(id=id).first()
            if record:
                db.delete(record)
                db.commit()

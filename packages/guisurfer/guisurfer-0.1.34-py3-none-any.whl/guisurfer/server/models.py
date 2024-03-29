from typing import List, Optional, Dict
import uuid
import time

from pydantic import BaseModel, Field
from threadmem.models import RoleThreadModel


class DesktopRuntimeModel(BaseModel):
    id: str
    name: str
    provider: str
    created: float
    updated: float
    metadata: dict = {}
    shared_with: Optional[List[str]] = None


class CreateDesktopRuntimeModel(BaseModel):
    name: str
    provider: str
    credentials: dict
    shared_with: Optional[List[str]] = None


class DesktopRuntimesModel(BaseModel):
    runtimes: List[DesktopRuntimeModel]


class AgentRuntimeModel(BaseModel):
    id: str
    name: str
    provider: str
    created: float
    updated: float
    metadata: dict = {}
    shared_with: Optional[List[str]] = None


class CreateAgentRuntimeModel(BaseModel):
    name: str
    provider: str
    credentials: dict
    metadata: dict = {}
    shared_with: Optional[List[str]] = None


class AgentRuntimesModel(BaseModel):
    runtimes: List[AgentRuntimeModel]


class SSHKeyModel(BaseModel):
    name: str
    public_key: str
    created: float
    id: str
    private_key: Optional[str] = None


class SSHKeyCreateModel(BaseModel):
    name: str
    public_key: str
    private_key: str


class SSHKeysModel(BaseModel):
    keys: List[SSHKeyModel]


class TaskCreateModel(BaseModel):
    description: str
    url: Optional[str] = None
    assigned_to: Optional[str] = None


class TaskUpdateModel(BaseModel):
    status: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None
    error: Optional[str] = None
    output: Optional[str] = None
    assigned_to: Optional[str] = None
    completed: Optional[float] = None
    version: Optional[str] = None


class TaskModel(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    description: str
    status: Optional[str] = None
    thread: Optional[RoleThreadModel] = None
    feed: Optional[RoleThreadModel] = None
    work_threads: Optional[List[RoleThreadModel]] = None
    assigned_to: Optional[str] = None
    url: Optional[str] = None
    created: float = Field(default_factory=time.time)
    started: float = 0.0
    completed: float = 0.0
    error: str = ""
    output: str = ""
    version: Optional[str] = None


class TasksModel(BaseModel):
    tasks: List[TaskModel]


class PostMessageModel(BaseModel):
    role: str
    msg: str
    images: List[str] = []
    thread: Optional[str] = None


class AddWorkThreadModel(BaseModel):
    public: bool
    name: Optional[str] = None
    metadata: Optional[dict] = None
    id: Optional[str] = None


class RemoveWorkThreadModel(BaseModel):
    id: str


class GCEProviderOptions(BaseModel):
    zone: str = "us-central1-a"
    region: str = "us-central1"


class EC2ProviderOptions(BaseModel):
    region: str = "us-east-1"


class CreateDesktopModel(BaseModel):
    runtime: str
    ssh_key_name: Optional[str] = None
    gce_opts: GCEProviderOptions = GCEProviderOptions()
    ec2_opts: EC2ProviderOptions = EC2ProviderOptions()
    name: Optional[str] = None
    image: Optional[str] = None
    memory: int = 4
    cpu: int = 2
    disk: str = "30gb"
    tags: Optional[Dict[str, str]] = None
    reserve_ip: bool = False


class V1UserProfile(BaseModel):
    email: Optional[str] = None
    display_name: Optional[str] = None
    handle: Optional[str] = None
    picture: Optional[str] = None
    created: Optional[int] = None
    updated: Optional[int] = None
    token: Optional[str] = None


class ActionModel(BaseModel):
    name: str
    parameters: dict = {}


class ActionResponseModel(BaseModel):
    action: str
    response: str
    parameters: dict = {}


class AgentModel(BaseModel):
    id: str
    name: str
    runtime: str
    type: str
    status: str
    created: float
    updated: float
    desktop: Optional[str] = None
    metadata: dict = {}
    secrets: dict = {}
    create_job_id: Optional[str] = None
    envs: dict = {}
    icon: Optional[str] = None


class AgentsModel(BaseModel):
    agents: List[AgentModel]


class CreateAgentModel(BaseModel):
    name: str
    runtime: str
    type: str
    desktop: Optional[str] = None
    desktop_request: Optional[CreateDesktopModel] = None
    metadata: dict = {}
    envs: dict = {}
    secrets: dict = {}
    wait_ready: bool = True
    icon: Optional[str] = None


class StartAgentModel(BaseModel):
    name: str
    wait_ready: bool = True


class EnvVarOptModel(BaseModel):
    name: str
    description: Optional[str] = None
    required: bool = False
    default: Optional[str] = None
    secret: bool = False


class CreateAgentTypeModel(BaseModel):
    id: str
    name: str
    description: str
    image: str
    env_opts: List[EnvVarOptModel] = []
    supported_runtimes: List[str] = []
    public: bool = False
    icon: Optional[str] = None


class AgentTypeModel(BaseModel):
    id: str
    name: str
    description: str
    image: str
    versions: Dict[str, str]
    env_opts: List[EnvVarOptModel] = []
    supported_runtimes: List[str] = []
    created: float
    updated: float
    public: bool = False
    icon: Optional[str] = None
    mem_request: Optional[str] = "500m"
    mem_limit: Optional[str] = "2gi"
    cpu_request: Optional[str] = "1"
    cpu_limit: Optional[str] = "4"
    gpu_mem: Optional[str] = None


class AgentTypesModel(BaseModel):
    types: List[AgentTypeModel]


class JobModel(BaseModel):
    id: str
    owner_id: str
    type: str
    status: str
    runtime: str
    name: str
    namespace: Optional[str] = None
    logs: Optional[str] = None
    result: Optional[str] = None
    created: float
    updated: float
    finished: float
    metadata: Dict[str, str] = {}


class JobsModel(BaseModel):
    jobs: List[JobModel]

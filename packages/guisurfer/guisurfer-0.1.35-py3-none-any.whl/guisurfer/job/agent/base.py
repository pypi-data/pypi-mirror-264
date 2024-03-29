from abc import ABC, abstractmethod

from guisurfer.server.models import CreateAgentModel, V1UserProfile


class CreateAgentJob(ABC):

    @abstractmethod
    def create_agent(
        self, data: CreateAgentModel, owner: V1UserProfile, api_key: str
    ) -> None:
        pass


class RestartAgentJob(ABC):

    @abstractmethod
    def restart_agent(self, name: str, owner: V1UserProfile, api_key: str) -> None:
        pass

import os
import requests

from guisurfer.server.models import CreateAgentModel, V1UserProfile


class Hub:
    """The Agentsea Hub"""

    def __init__(self, hub_url: str = "https://hub.agentsea.ai") -> None:
        self.hub_url = os.getenv("AGENTSEA_HUB_URL", hub_url)

    def get_api_key(self, user: V1UserProfile) -> str:

        hub_key_url = f"{self.hub_url}/v1/users/me/keys"
        headers = {"Authorization": f"Bearer {user.token}"}
        response = requests.get(hub_key_url, headers=headers)
        response.raise_for_status()
        key_data = response.json()

        return key_data["key"]

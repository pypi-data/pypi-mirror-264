from guisurfer.agent.types import AgentType
from guisurfer.server.models import EnvVarOptModel


def ensure_common_models():
    try:
        AgentType(
            name="SurfDino",
            description="A GUI surfer which uses Grounding Dino and OCR",
            image="us-central1-docker.pkg.dev/agentsea-dev/guisurfer/surfdino:latest",
            supported_runtimes=["gke"],
            env_opts=[
                EnvVarOptModel(
                    name="OPENAI_API_KEY",
                    description="OpenAI API Key",
                    required=True,
                    secret=True,
                ),
            ],
            owner_id="patrick.barker@kentauros.ai",
            public=True,
            icon="https://storage.googleapis.com/guisurfer-assets/surf_dino2.webp",
            mem_request="2Gi",
            mem_limit="8Gi",
            cpu_request="2",
            cpu_limit="8",
        )
    except Exception as e:
        print(
            f"failed to create common models: {e} \n this can likely be ignored if they exist"
        )
        return
    print("common models created")


def boot_seq():
    ensure_common_models()

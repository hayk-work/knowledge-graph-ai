from langsmith import Client
from app.config import LANGSMITH_API_KEY, LANGSMITH_ENDPOINT, LANGSMITH_PROJECT

client = Client(
    api_key=LANGSMITH_API_KEY,
    api_url=LANGSMITH_ENDPOINT
)


def log_run(name: str, inputs: dict, outputs: dict):
    return client.create_run(
        name=name,
        inputs=inputs,
        outputs=outputs,
        project_name=LANGSMITH_PROJECT
    )
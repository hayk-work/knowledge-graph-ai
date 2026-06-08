from langsmith import Client

from app.config import LANGCHAIN_API_KEY, LANGCHAIN_ENDPOINT, LANGCHAIN_PROJECT

client = Client(
    api_key=LANGCHAIN_API_KEY,
    api_url=LANGCHAIN_ENDPOINT,
)


def log_run(name: str, inputs: dict, outputs: dict):
    return client.create_run(
        name=name,
        inputs=inputs,
        outputs=outputs,
        project_name=LANGCHAIN_PROJECT,
    )

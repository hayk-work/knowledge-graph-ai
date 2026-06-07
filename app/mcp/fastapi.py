import requests

BASE_URL = "http://localhost:8000"


def ask(question: str):
    return requests.post(
        f"{BASE_URL}/ask",
        json={"question": question}
    ).json()


def health():
    return requests.get(f"{BASE_URL}/health").json()
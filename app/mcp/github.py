import requests

from app.config import GITHUB_TOKEN

BASE_URL = "https://api.github.com"


def list_repo_files(repo: str):
    url = f"{BASE_URL}/repos/{repo}/contents"
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    return requests.get(url, headers=headers).json()


def get_file(repo: str, path: str):
    url = f"{BASE_URL}/repos/{repo}/contents/{path}"
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    return requests.get(url, headers=headers).json()
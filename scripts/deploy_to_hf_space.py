import os

from huggingface_hub import HfApi

SPACE_ID = os.environ.get("HF_SPACE_ID", "vanshika-ramchandani/askdocs-ai-backend")
TOKEN = os.environ["HF_DEPLOY_TOKEN"]

api = HfApi(token=TOKEN)

api.create_repo(
    repo_id=SPACE_ID,
    repo_type="space",
    space_sdk="docker",
    exist_ok=True,
)

api.upload_folder(
    repo_id=SPACE_ID,
    repo_type="space",
    folder_path=".",
    path_in_repo=".",
    allow_patterns=["backend/**", "requirements.txt", "Dockerfile"],
    ignore_patterns=["**/__pycache__/**", "**/*.pyc", "backend/data/**"],
)

api.upload_file(
    path_or_fileobj="space/README.md",
    path_in_repo="README.md",
    repo_id=SPACE_ID,
    repo_type="space",
)

print(f"Deployed to https://huggingface.co/spaces/{SPACE_ID}")

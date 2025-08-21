from __future__ import annotations
import os, base64, fnmatch
from typing import Iterable, Tuple
from github import Github

def list_repo_files(repo_full: str, globs: list[str]) -> Iterable[Tuple[str, bytes]]:
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        return []
    gh = Github(token)
    repo = gh.get_repo(repo_full)
    tree = repo.get_git_tree(repo.default_branch, recursive=True).tree
    for item in tree:
        if item.type != "blob":
            continue
        path = item.path
        if globs and not any(fnmatch.fnmatch(path, g) for g in globs):
            continue
        try:
            blob = repo.get_git_blob(item.sha)
            data = base64.b64decode(blob.content)
            yield path, data
        except Exception:
            continue

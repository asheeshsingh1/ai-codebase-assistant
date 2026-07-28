from pathlib import Path

from git import Repo


class GitService:
    def clone(self, git_url: str, destination: Path) -> None:
        destination.parent.mkdir(parents=True, exist_ok=True)

        Repo.clone_from(
            git_url,
            destination,
        )
from pathlib import Path

from app.db.models.repository import Repository
from app.db.models.repository_file import RepositoryFile
from app.repositories.repository_file import RepositoryFileRepository
from app.services.file_scanner import FileScanner


class FileIndexerService:
    def __init__(
        self,
        scanner: FileScanner,
        repository_file_repo: RepositoryFileRepository,
    ):
        self.scanner = scanner
        self.repository_file_repo = repository_file_repo

    async def index_repository(
        self,
        repository: Repository,
    ) -> None:
        if repository.local_path is None:
            raise ValueError("Repository has no local path.")

        print("Scanning repository...")
        files = self.scanner.scan(
            Path(repository.local_path),
        )
        print(f"Found {len(files)} files")
        
        print("Building RepositoryFile objects...")
        repository_files = [
            RepositoryFile(
                repository_id=repository.id,
                relative_path=file["relative_path"],
                extension=file["extension"],
                language=file["language"],
                size=file["size"],
                checksum=file["checksum"],
            )
            for file in files
        ]

        print("Deleting existing metadata...")
        try:
            await self.repository_file_repo.delete_by_repository(
                repository.id
            )
        except Exception as e:
            print("DELETE FAILED:", repr(e))
            raise

        print("Bulk inserting...")
        await self.repository_file_repo.bulk_create(
            repository_files
        )
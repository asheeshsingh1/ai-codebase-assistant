from __future__ import annotations

import hashlib
from pathlib import Path


class FileScanner:
    IGNORE_DIRS = {
        ".git",
        ".idea",
        ".vscode",
        "__pycache__",
        "node_modules",
        ".venv",
        "venv",
        "dist",
        "build",
        ".mypy_cache",
        ".pytest_cache",
    }

    ALLOWED_EXTENSIONS = {
        ".py",
        ".js",
        ".ts",
        ".tsx",
        ".jsx",
        ".java",
        ".go",
        ".rs",
        ".cpp",
        ".cc",
        ".c",
        ".h",
        ".hpp",
        ".cs",
        ".php",
        ".rb",
        ".swift",
        ".kt",
        ".kts",
        ".scala",
        ".sql",
        ".sh",
        ".yaml",
        ".yml",
        ".json",
        ".toml",
        ".xml",
        ".md",
        ".txt",
    }

    EXTENSION_LANGUAGE_MAP = {
        ".py": "python",
        ".js": "javascript",
        ".ts": "typescript",
        ".tsx": "typescript",
        ".jsx": "javascript",
        ".java": "java",
        ".go": "go",
        ".rs": "rust",
        ".cpp": "cpp",
        ".cc": "cpp",
        ".c": "c",
        ".h": "c",
        ".hpp": "cpp",
        ".cs": "csharp",
        ".php": "php",
        ".rb": "ruby",
        ".swift": "swift",
        ".kt": "kotlin",
        ".kts": "kotlin",
        ".scala": "scala",
        ".sql": "sql",
        ".sh": "shell",
        ".yaml": "yaml",
        ".yml": "yaml",
        ".json": "json",
        ".toml": "toml",
        ".xml": "xml",
        ".md": "markdown",
        ".txt": "text",
    }

    def scan(self, repository_path: Path) -> list[dict]:
        files = []

        for file_path in repository_path.rglob("*"):
            if not file_path.is_file():
                continue

            if self._should_ignore(file_path):
                continue

            extension = file_path.suffix.lower()

            if extension not in self.ALLOWED_EXTENSIONS:
                continue

            files.append(
                {
                    "relative_path": str(file_path.relative_to(repository_path)),
                    "extension": extension,
                    "language": self.EXTENSION_LANGUAGE_MAP.get(extension),
                    "size": file_path.stat().st_size,
                    "checksum": self._calculate_checksum(file_path),
                }
            )

        return files

    def _should_ignore(self, file_path: Path) -> bool:
        return any(part in self.IGNORE_DIRS for part in file_path.parts)

    def _calculate_checksum(self, file_path: Path) -> str:
        sha = hashlib.sha256()

        with open(file_path, "rb") as f:
            while chunk := f.read(8192):
                sha.update(chunk)

        return sha.hexdigest()

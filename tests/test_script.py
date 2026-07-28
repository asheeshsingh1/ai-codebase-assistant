from pathlib import Path

from app.services.file_scanner import FileScanner

scanner = FileScanner()

repo_path = Path("storage/repos/7f581937-8d59-482b-9a81-92daaab59f22")

files = scanner.scan(repo_path)

print(f"Found {len(files)} files")

for file in files[:20]:
    print(file)
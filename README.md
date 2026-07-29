# Important Commands:

```bash
poetry run alembic revision --autogenerate -m "create file_chunks table"
```
```bash
poetry run alembic upgrade head
```
```bash
python -m tests.test_script
```
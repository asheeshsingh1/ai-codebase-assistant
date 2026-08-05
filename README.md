# AI Codebase Assistant
### Important Commands:

* To run the pgvector container locally
```bash
docker compose up -d
```

* Generate Migration
```bash
poetry run alembic revision --autogenerate -m "create table_name table"
```

* Apply Migration
```bash
poetry run alembic upgrade head
```

* Run Test file
```bash
python -m tests.test_script
```

* Start app locally
```bash
poetry run uvicorn app.main:app --reload
```

### Features/Enhancements to be done:
1. Incremental Repository Sync
2. Streaming + Async Jobs
3. Containerization(Docker) for deployment
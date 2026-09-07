# AI Codebase Assistant

An AI-powered codebase assistant that indexes Git repositories, performs semantic code search, and answers repository-specific questions using a Retrieval-Augmented Generation (RAG) pipeline.

## Features

- Git repository indexing
- Repository-aware code chunking
- Semantic code search using embeddings
- PostgreSQL + pgvector for vector storage
- LLM-powered repository Q&A
- Persistent chat history
- Source citations with file and line references
- Monaco-based code viewer with citation highlighting
- Docker-based self-hosted deployment

## Architecture

```text
                        ┌──────────────────┐
                        │     Frontend     │
                        │ Next.js + React  │
                        └────────┬─────────┘
                                 │
                                 ▼
                        ┌──────────────────┐
                        │     FastAPI      │
                        │     Backend      │
                        └────────┬─────────┘
                                 │
              ┌──────────────────┼──────────────────┐
              │                  │                  │
              ▼                  ▼                  ▼
       ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
       │ Git Service │    │ RAG/Search  │    │ LLM Service │
       └──────┬──────┘    └──────┬──────┘    └──────┬──────┘
              │                  │                  │
              ▼                  ▼                  ▼
       ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
       │ Repository  │    │ PostgreSQL  │    │ Gemini API  │
       │   Storage   │    │ + pgvector  │    │             │
       └─────────────┘    └─────────────┘    └─────────────┘
```

# Running with Docker

The recommended way to run the application is with Docker Compose.

## Prerequisites

Install:

- Docker
- Docker Compose

You do not need Python, Poetry, Node.js, or PostgreSQL installed locally when using the Docker setup.

## 1. Clone the repository

Because the frontend is maintained as a Git submodule:

```bash
git clone --recurse-submodules https://github.com/asheeshsingh1/ai-codebase-assistant.git
cd ai-codebase-assistant
```

If you already cloned the repository without submodules:

```bash
git submodule update --init --recursive
```

## 2. Configure environment variables

Create a `.env` file:

```bash
cp .env.example .env
```

Update `.env` with your API keys and model configuration.

Example:

```env
# LLM
LLM_PROVIDER=gemini
LLM_MODEL=gemini-3.6-flash
GEMINI_API_KEY=your_gemini_api_key

# Embeddings
EMBEDDING_PROVIDER=openrouter
EMBEDDING_MODEL=nvidia/nemotron-3-embed-1b:free
OPENROUTER_API_KEY=your_openrouter_api_key
```

> API keys are supplied at container runtime and are not included in the Docker images.

## 3. Start the application

```bash
docker compose up -d
```

Docker Compose will start:

- PostgreSQL + pgvector
- Backend API
- Frontend

The application uses the published Docker Hub images:

```text
asheeshsingh01/codebase-assistant:be
asheeshsingh01/codebase-assistant:fe
```

## 4. Check running containers

```bash
docker compose ps
```

You should see:

```text
ai-codebase-db
ai-codebase-backend
ai-codebase-frontend
```

## 5. Access the application

Frontend:

```text
http://localhost:3000
```

Backend API:

```text
http://localhost:8000
```

API documentation:

```text
http://localhost:8000/docs
```

Health check:

```text
http://localhost:8000/health
```

## 6. Stop the application

```bash
docker compose down
```

To remove the database and repository volumes as well:

```bash
docker compose down -v
```

> Warning: removing volumes deletes persisted PostgreSQL data and indexed repositories.

# Local Development

If you want to develop the backend without Docker:

## Prerequisites

- Python 3.12+
- Poetry
- PostgreSQL with pgvector

Start PostgreSQL:

```bash
docker compose up -d postgres
```

Install Python dependencies:

```bash
poetry install
```

Apply database migrations:

```bash
poetry run alembic upgrade head
```

Start the backend:

```bash
poetry run uvicorn app.main:app --reload
```

The backend will be available at:

```text
http://localhost:8000
```

# Database Migrations

Generate a migration after modifying database models:

```bash
poetry run alembic revision --autogenerate -m "create table_name table"
```

Apply migrations:

```bash
poetry run alembic upgrade head
```

# Running Tests

Run the test script:

```bash
python -m tests.test_script
```

# Docker Image Development

To build the images locally instead of pulling them from Docker Hub:

### Backend

```bash
docker build -t asheeshsingh01/codebase-assistant:be .
```

### Frontend

```bash
docker build -t asheeshsingh01/codebase-assistant:fe ./frontend
```

# Persistent Data

Docker Compose uses named volumes to persist application data.

```text
postgres_data
    └── PostgreSQL database + pgvector data

repositories
    └── Cloned and indexed Git repositories
```

Restarting the containers does not remove this data:

```bash
docker compose down
docker compose up -d
```

# Current Enhancements

- [x] Docker containerization
- [x] Docker Hub images
- [ ] Incremental Repository Sync
- [ ] Streaming Responses
- [ ] Asynchronous Background Indexing Jobs

# Tech Stack

### Backend

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- pgvector
- Alembic
- Poetry

### Frontend

- Next.js
- React
- TypeScript
- Monaco Editor
- TanStack Query
- Tailwind CSS

### AI

- Retrieval-Augmented Generation (RAG)
- Vector embeddings
- Gemini
- OpenRouter

### Infrastructure

- Docker
- Docker Compose
- Git

# Project Structure

```text
ai-codebase-assistant/
│
├── app/
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── repositories/
│   └── services/
│
├── alembic/
├── frontend/
├── tests/
├── Dockerfile
├── docker-compose.yml
├── alembic.ini
├── pyproject.toml
├── poetry.lock
├── .env.example
└── README.md
```

# License

This project is for educational and portfolio purposes.
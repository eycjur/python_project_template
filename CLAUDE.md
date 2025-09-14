# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

**Run tests:**
```bash
make test
# or directly with pytest
pytest -sv
```

**Lint and format code:**
```bash
make lint  # runs both ruff and mypy
make ruff  # ruff check --fix . && ruff format .
make mypy  # type checking
```

**Development workflow:**
```bash
make up      # start docker containers
make down    # stop containers
make exec    # shell into container
make restart # restart containers
```

**Run pre-commit checks:**
```bash
make pre-commit-run-all
```

## Architecture Overview

This is a Python web application template implementing **Onion Architecture** with multiple UI framework options and cloud deployment support.

### Core Architecture
- **Domain Layer:** `app/domain/message/` - Business entities (Message, ID) and repository interfaces (IMessageRepository)
- **Infrastructure Layer:** `app/infrastructure/repository/message/` - Database implementations:
  - `sqlite_message_repository.py` - SQLite implementation
  - `gcp_message_repository.py` - Firestore implementation
  - `aws_message_repository.py` - DynamoDB implementation
  - `azure_message_repository.py` - CosmosDB implementation
- **Use Case Layer:** `app/usecase/` - Business logic orchestration:
  - `register.py` - Message registration use case
  - `history.py` - Message history use case
  - `error.py` - Error handling use case
- **Presentation Layer:** `app/presentation/` - Multiple UI frameworks:
  - `cli/` - Command-line interface using Typer
  - `fastapi/` - REST API with frontend
  - `flask/` - Server-side rendering
  - `streamlit/` - Data visualization framework
  - `dash/` - Interactive dashboard framework

### Dependency Injection
The project uses a sophisticated DI system (`app/di.py`) that automatically selects database implementations based on the runtime environment:
- **LOCAL/GITHUB_ACTIONS:** SQLite (`LocalModule`) - File-based database
- **TEST:** SQLite in-memory (`TestModule`) - In-memory database for tests
- **GCP:** Firestore (`GCPModule`) - Cloud Firestore NoSQL database
- **AWS:** DynamoDB (`AWSModule`) - AWS NoSQL database service
- **AZURE:** CosmosDB (`AzureModule`) - Azure's multi-model database service

Environment detection happens automatically via `RunEnv.judge_from_env()` in `app/settings.py` by checking specific environment variables:
- `PYTEST_CURRENT_TEST` - Test environment
- `GITHUB_ACTIONS` - GitHub Actions CI/CD
- `K_SERVICE` - Google Cloud Run
- `AWS_EXECUTION_ENV` - AWS App Runner
- `CONTAINER_APP_REPLICA_NAME` - Azure Container Apps

### Multiple UI Frameworks
The same business logic is exposed through different presentation layers:
- **FastAPI:** REST API with frontend in `app/presentation/fastapi/frontend/`
- **Flask:** Server-side rendering
- **Streamlit/Dash:** Data visualization frameworks
- **CLI:** Command-line interface using Typer

### Configuration Management
- Environment-specific settings in `app/settings.py`
- Cloud-specific logger configurations in `app/logger/`
- Secrets management varies by cloud platform (AWS Secrets Manager, GCP Secret Manager, etc.)

### Testing Setup
- Tests automatically use in-memory SQLite via DI container reset in `tests/conftest.py`
- **Unit tests:** `tests/unit/` - Domain layer tests (e.g., `tests/unit/domain/message/`)
- **E2E tests:** `tests/e2e/` - End-to-end API tests (`test_fastapi.py`, `test_flask.py`)
- DI container is reset before each test via `reset_injector()` to ensure isolation
- Test configuration uses `TestModule` which provides in-memory SQLite database

### Cloud Deployment
Infrastructure as Code using Terraform for GCP, AWS (App Runner & Lambda), and Azure Container Apps. Each platform has specific deployment scripts in the Makefile.

## Project Structure Notes
- `app/` - Main application directory with onion architecture layers
- `tests/` - Unit tests (`unit/`) and end-to-end tests (`e2e/`)
- `credentials/` - Cloud service account files (not in git)
- `infra/` - Terraform modules for each cloud platform (`gcp/`, `aws_apprunner/`, `aws_lambda/`)
- `docs/` - Architecture diagrams and requirements documentation
- `db/` - Local SQLite database file
- `.devcontainer/` - VS Code development container configuration
- `compose.yml` - Docker Compose configuration for local development

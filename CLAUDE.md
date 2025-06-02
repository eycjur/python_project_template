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
```

**Run pre-commit checks:**
```bash
make pre-commit-run-all
```

## Architecture Overview

This is a Python web application template implementing **Onion Architecture** with multiple UI framework options and cloud deployment support.

### Core Architecture
- **Domain Layer:** `app/domain/` - Business entities and repository interfaces
- **Infrastructure Layer:** `app/infrastructure/repository/` - Database implementations (SQLite, Firestore, DynamoDB, CosmosDB)  
- **Use Case Layer:** `app/usecase/` - Business logic orchestration
- **Presentation Layer:** `app/presentation/` - Multiple UI frameworks (FastAPI, Flask, Streamlit, Dash, CLI)

### Dependency Injection
The project uses a sophisticated DI system (`app/di.py`) that automatically selects database implementations based on the runtime environment:
- **Local/Test:** SQLite
- **GCP:** Firestore  
- **AWS:** DynamoDB
- **Azure:** CosmosDB

Environment detection happens automatically via environment variables in `app/settings.py`.

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
- Tests automatically use in-memory SQLite via DI container reset in `conftest.py`
- Both unit tests (`tests/unit/`) and e2e tests (`tests/e2e/`) available
- DI container is reset before each test to ensure isolation

### Cloud Deployment
Infrastructure as Code using Terraform for GCP, AWS (App Runner & Lambda), and Azure Container Apps. Each platform has specific deployment scripts in the Makefile.

## Project Structure Notes
- `credentials/` - Cloud service account files (not in git)
- `infra/` - Terraform modules for each cloud platform
- `scripts/sample/` - Example/demo scripts
- `docs/` - Architecture diagrams and requirements documentation

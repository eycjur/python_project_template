# GitHub Copilot Instructions

This Python project implements **Onion Architecture** with multi-cloud deployment support and multiple UI framework options. Follow these guidelines when generating code.

## Architecture Overview

### Core Layers (Onion Architecture)
- **Domain Layer** (`app/domain/`): Entities and repository interfaces (innermost layer)
- **Infrastructure Layer** (`app/infrastructure/`): Database implementations, external services
- **Usecase Layer** (`app/usecase/`): Business logic orchestration
- **Presentation Layer** (`app/presentation/`): UI frameworks and controllers (outermost layer)

**Dependency Direction**: Always point inward. Outer layers depend on inner layers, never the reverse.

### Dependency Injection Pattern
- Use `injector` library with `@inject` decorator
- All usecases and controllers use DI via constructor injection
- Repository implementations are automatically selected by environment
- Always inject interfaces, not concrete implementations

```python
from injector import inject
from app.domain.message.message_repository import IMessageRepository

class RegisterUsecase:
    @inject
    def __init__(self, message_repository: IMessageRepository) -> None:
        self._message_repository = message_repository
```

## Code Style and Conventions

### Type Hints
- **ALWAYS** use strict type hints for all functions, methods, and variables
- Use `from typing import` imports when needed
- Return types are mandatory

```python
def execute(self, message: Message) -> str:
    # Implementation
```

### Naming Conventions
- Classes: PascalCase (`MessageRepository`)
- Functions/methods: snake_case (`find_all`)
- Constants: UPPER_SNAKE_CASE (`BASE_DIR`)
- Private attributes: leading underscore (`self._repository`)
- Interface prefix: `I` (`IMessageRepository`)

### Documentation
- Use Japanese docstrings for all public methods
- Follow Google-style docstring format
- Include Args and Returns sections

```python
def execute(self, message: Message) -> str:
    """メッセージを保存する

    Args:
        message (Message): 保存するメッセージ

    Returns:
        str: 保存完了メッセージ
    """
```

## Domain Layer Patterns

### Entities
- Encapsulate business logic and data
- Use private attributes with public properties
- Implement `__eq__` based on entity ID
- Provide `from_repository` and `to_repository` class methods

```python
class Message:
    def __init__(self, content: str, *, id: Optional[ID] = None) -> None:
        self._content = content
        self._id = id if id is not None else ID()
    
    @property
    def content(self) -> str:
        return self._content
    
    @classmethod
    def from_repository(cls, data: dict[str, str]) -> "Message":
        return cls(data["content"], id=ID(data["id"]))
    
    def to_repository(self) -> dict[str, str]:
        return {"id": self.id, "content": self.content}
```

### Value Objects
- Use frozen dataclasses for immutable values
- Provide default factory for generated values (like UUIDs)

```python
@dataclass(eq=True, frozen=True)
class ID:
    value: str = field(default_factory=lambda: str(uuid.uuid4()))
```

### Repository Interfaces
- Define abstract base classes with `@abstractmethod`
- Keep interfaces minimal and focused
- Use domain language in method names

```python
from abc import ABC, abstractmethod

class IMessageRepository(ABC):
    @abstractmethod
    def upsert(self, message: Message) -> None:
        pass
    
    @abstractmethod
    def find_all(self, limit: int = 10) -> list[Message]:
        pass
```

## Infrastructure Layer

### Repository Implementations
- Implement repository interfaces for specific databases
- Handle data conversion between domain entities and storage format
- Include proper error handling and logging
- Use consistent naming: `{Platform}MessageRepository`

Available implementations:
- `SQLiteMessageRepository` (Local/Test)
- `GCPMessageRepository` (Firestore)
- `AWSMessageRepository` (DynamoDB)
- `AzureMessageRepository` (CosmosDB)

## Usecase Layer

### Business Logic
- Single responsibility per usecase
- Use DI for repository dependencies
- Return simple data types or domain entities
- Include comprehensive logging

```python
class RegisterUsecase:
    @inject
    def __init__(self, message_repository: IMessageRepository) -> None:
        self._message_repository = message_repository
    
    def execute(self, message: Message) -> str:
        self._message_repository.upsert(message)
        logger.info(f"Message: {message.content}")
        return "データの保存が完了しました。"
```

## Presentation Layer

### Multiple UI Frameworks Support
Generate code that works with these presentation options:
- **FastAPI**: REST API with OpenAPI docs
- **Flask**: Server-side rendering with templates
- **Streamlit**: Data science/analytics UI
- **Dash**: Interactive dashboards
- **CLI**: Typer-based command line interface

### Controller Pattern
- Controllers handle HTTP/UI specific concerns
- Use DI to inject usecases
- Convert between view models and domain entities
- Handle errors at presentation boundary

```python
class RegisterController:
    @inject
    def __init__(self, register_usecase: RegisterUsecase):
        self._register_usecase = register_usecase
    
    def execute(self, request: RegisterRequest) -> RegisterResponse:
        result = self._register_usecase.execute(request.to_message())
        return RegisterResponse(text=result)
```

### FastAPI Specific
- Use dependency injection with `Depends(get_injector)`
- Define request/response models with Pydantic
- Include proper HTTP status codes and error handling

```python
@router.post("/messages")
def register(
    request: RegisterRequest, 
    injector: Annotated[Injector, Depends(get_injector)]
) -> RegisterResponse:
    controller = injector.get(RegisterController)
    return controller.execute(request)
```

## Environment and Configuration

### Multi-Cloud Support
The application automatically detects and configures for different environments:
- **Local**: SQLite database
- **GCP**: Cloud Run + Firestore
- **AWS**: App Runner/Lambda + DynamoDB
- **Azure**: Container Apps + CosmosDB

### Settings Pattern
- Use `environs` for environment variable parsing
- Implement environment detection in `RunEnv.judge_from_env()`
- Load cloud-specific secrets (AWS Secrets Manager, etc.)

## Testing

### Test Structure
- Unit tests in `tests/unit/` matching `app/` structure
- E2E tests in `tests/e2e/`
- Use pytest with parametrized tests
- Reset DI container before each test (handled by `conftest.py`)

### Test Patterns
```python
@pytest.mark.parametrize(
    "message",
    [Message("content"), Message("")],
    ids=["normal_message", "empty_message"],
)
def test_message_encode_decode_ok(message: Message) -> None:
    encoded = message.to_repository()
    decoded = Message.from_repository(encoded)
    assert message == decoded
```

## Development Commands

Use these Make commands for development:
- `make test`: Run tests with pytest
- `make lint`: Run ruff linting and formatting
- `make mypy`: Type checking
- `make pre-commit-run-all`: Run all pre-commit hooks

## Key Libraries and Tools

- **DI**: `injector` - Dependency injection container
- **Web**: `fastapi`, `flask`, `streamlit`, `dash` - Multiple UI options
- **CLI**: `typer` - Command line interface
- **Config**: `environs`, `python-dotenv` - Environment management
- **Cloud**: `boto3`, `google-cloud-firestore`, `azure-cosmos` - Cloud services
- **Testing**: `pytest` - Testing framework
- **Linting**: `ruff`, `mypy` - Code quality tools

## Important Reminders

1. **Always follow Onion Architecture** - Dependencies point inward only
2. **Use DI everywhere** - Inject dependencies, don't instantiate directly
3. **Type everything** - Strict type hints are mandatory
4. **Environment agnostic** - Code should work across all cloud platforms
5. **Test isolation** - Each test should be independent
6. **Japanese documentation** - Use Japanese for docstrings and comments
7. **Error handling** - Include proper logging and error handling
8. **Repository pattern** - Always use repository interfaces, never direct DB access

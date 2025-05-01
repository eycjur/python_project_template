from pydantic import BaseModel


class ErrorResponse(BaseModel):
    description: str

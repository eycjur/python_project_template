import os
from typing import Dict

import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")  # type: ignore
def home() -> Dict:
    return {"message": "Sample App"}


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000)),
        reload=True,
    )

from typing import Dict

from fastapi import FastAPI

app = FastAPI()


@app.get("/")  # type: ignore
def home() -> Dict:
    return {"message": "Sample App"}


if __name__ == "__main__":
    app.run()

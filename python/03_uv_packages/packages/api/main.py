import os
from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn

load_dotenv()


app = FastAPI()


@app.get("/headlines")
def get_headlines(limit: int = 5):
    return {"headlines": fetch_headlines(limit)}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "8000")),
    )

from contextlib import asynccontextmanager
from fastapi import Body, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from db import Base, add_request_data, engine, get_user_requests
from gemini_client import get_answer_from_gemini


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    print("All tables are created.")
    yield


app = FastAPI(title="My Startup", lifespan=lifespan)


@app.get("/requests")
def get_my_requests(request: Request):
    user_ip_address = request.client.host
    user_requests = get_user_requests(ip_address=user_ip_address)
    return user_requests


@app.post("/requests")
def send_prompt(
    request: Request,
    prompt: str = Body(embed=True),
):
    answer = get_answer_from_gemini(prompt)
    add_request_data(ip_address=request.client.host, prompt=prompt, response=answer)
    return {"answer": answer}


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

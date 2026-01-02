from contextlib import contextmanager, asynccontextmanager
from fastapi import FastAPI, Body, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from openAI_client import  get_answer_from_prompt
from db import Base, engine, get_user_requests, add_user_data

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    print("All tables created")
    yield
app = FastAPI(
    title="OpenAI API pet project",
    version="0.1.0",
    lifespan=lifespan
)


@app.get("/", summary="Приветсвтвие", tags=["Welcome"])
async def root():
    return {"message": "Hello in my pet project!!!!"}

@app.get("/requests", summary="Получение своих запросов", tags=["OpenAI"])
def get_requests(request: Request):
    user_requests = get_user_requests(ip_address=request.client.host)
    return [
        {
            "id": r.id,
            "ip_address": r.ip_address,
            "prompt": r.prompt,
            "response": r.response,
        }
        for r in user_requests
    ]

@app.post("/requests", summary="Отправка prompt в OpenAI", tags=["OpenAI"])
async def send_prompt(
        request: Request,
        prompt: str = Body(embed=True)
):
    answer = get_answer_from_prompt(prompt)
    add_user_data(
        ip_address=request.client.host,
        prompt=prompt,
        response=answer,
    )
    return {"answer": {answer}}

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://192.168.3.236:5500",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

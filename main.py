from contextlib import asynccontextmanager

from fastapi import FastAPI, Body, Request
from fastapi.middleware.cors import CORSMiddleware

from openAI_client import get_answer_from_prompt
from db import init_models, get_user_requests, add_user_data

from schemas import ChatInput, ChatOutput, ChatHistoryItem


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_models()
    print("All tables created")
    yield

app = FastAPI(
    title="OpenAI API pet project",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/", summary="Приветсвтвие", tags=["Welcome"])
async def root():
    return {"message": "Hello in my pet project!!!!"}

@app.get(
    "/requests",
    summary="Получение своих запросов",
    tags=["OpenAI"],
    response_model=list[ChatHistoryItem],
)
async def get_requests(request: Request):
    user_requests = await get_user_requests(ip_address=request.client.host)
    return user_requests

@app.post(
    "/requests",
    summary="Отправка prompt в OpenAI",
    tags=["OpenAI"],
    response_model=ChatOutput,
)
async def send_prompt(
        request: Request,
        user_input: ChatInput,
):
    # Вызов внешнего ИИ-сервиса
    answer = get_answer_from_prompt(user_input.prompt)

    # Асинхронная запись в БД
    await add_user_data(
        ip_address=request.client.host,
        prompt=user_input.prompt,
        response=answer,
    )
    return ChatOutput(answer=answer)

# CORS, с порта 5500 доступ к API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://192.168.3.236:5500",
        "*",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

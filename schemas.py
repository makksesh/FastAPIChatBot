from pydantic import BaseModel, ConfigDict

# DTO для входящего запроса
class ChatInput(BaseModel):
    prompt: str

# DTO для ответа
class ChatOutput(BaseModel):
    answer: str

# DTO для элемента истории
class ChatHistoryItem(BaseModel):
    id: int
    ip_address: str
    prompt: str
    response: str

    model_config = ConfigDict(from_attributes=True)

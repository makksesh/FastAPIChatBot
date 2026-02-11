import pytest
from unittest.mock import patch


# Тест 1: Проверка ручки / (Health check)
@pytest.mark.asyncio
async def test_root(client):
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello in my pet project!!!!"}


# Тест 2: Полный цикл (Запрос -> Мок AI -> БД -> Ответ)
@pytest.mark.asyncio
async def test_send_prompt_integration(client):
    # Данные для отправки
    payload = {"prompt": "Как дела?"}

    # Фейковый ответ от нейросети
    mock_ai_response = "У меня все отлично, я тестовый бот!"

    # Используем patch, чтобы перехватить вызов get_answer_from_prompt ВНУТРИ main.py
    # Важно: патчим именно там, где функция ИСПОЛЬЗУЕТСЯ (в данном проекте main), а не где объявлена
    with patch("main.get_answer_from_prompt", return_value=mock_ai_response) as mock_func:
        # 1. Делаем POST запрос
        response = await client.post("/requests", json=payload)

        # 2. Проверяем статус и ответ API
        assert response.status_code == 200
        data = response.json()
        assert data["answer"] == mock_ai_response

        # 3. Проверяем, что реальный запрос к AI не уходил, а вызвался мок
        mock_func.assert_called_once_with("Как дела?")

        # 4. Проверяем, что запись сохранилась в БД (Интеграция с БД)
        # Получаем историю запросов
        history_response = await client.get("/requests")
        history_data = history_response.json()

        assert len(history_data) == 1
        assert history_data[0]["prompt"] == "Как дела?"
        assert history_data[0]["response"] == mock_ai_response

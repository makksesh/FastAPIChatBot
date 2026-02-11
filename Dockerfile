FROM python:3.14.2-slim
LABEL authors="makksesh"

WORKDIR /app

COPY requirements.txt .

# --no-cache-dir уменьшает размер образа, не сохраняя кэш pip.
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
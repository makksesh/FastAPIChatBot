# 🚀 FastAPI + React ИИ Чат

Полноценный чат с ИИ (OpenAI) — бэкенд на **FastAPI**, фронтенд на **React + Vite**.

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-blue?logo=fastapi)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-green?logo=react)](https://react.dev)
[![Vite](https://img.shields.io/badge/Vite-5-orange?logo=vite)](https://vitejs.dev)

## ✨ Демо

- **Backend API**: `http://localhost:8000/docs` (Swagger)  
- **Frontend**: `http://localhost:5500` (чат ИИ)  
- **LAN доступ**: `http://192.168.x.x:5500`

## 🛠️ Быстрый старт

### Backend (FastAPI)
```bash
pip install -r requirements.txt
cp config.py.example config.py  # добавить OPENAI_API_KEY
uvicorn main:app --reload
```

### Frontend (React + Vite)
```bash
cd chat-frontend
npm install
npm run dev  
```



## 📁 Структура проекта

```
FastAPIProject/
├── README.md                 # 📖 Документация
├── .gitignore               # 🚫 Игнор секретов
├── requirements.txt         # 🐍 Python зависимости
├── config.py.example        # 🔑 Шаблон API ключей
│
├── main.py                  # ⚡ FastAPI сервер
├── db.py                    # 🗄️ SQLAlchemy + SQLite
├── openAI_client.py         # 🤖 OpenAI клиент
│
└── chat-frontend/           # 🎨 React + Vite
    ├── package.json         # 📦 Node зависимости
    ├── vite.config.js       # 🌐 Порт 5500 + LAN
    ├── index.html
    └── src/
        ├── App.jsx          # 💬 Чат UI
        ├── App.css          # 🎨 Пепельно-розовый дизайн
        └── main.jsx
```

**💡 config.py.example** — скопируй и добавь `OPENAI_API_KEY`.


>### 🔧 Особенности 
> ✅ CORS для localhost:5500 + LAN IP\\\
> ✅ История чатов сохраняется в SQLite\\\
> ✅ React Query для запросов\\\
> ✅ Пепельно-розовый дизайн\\\
> ✅ LAN доступ (телефон/планшет)
	
	


### 📄 Лицензия
MIT © 2026 

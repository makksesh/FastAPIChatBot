import { useEffect, useState, useRef } from 'react'
import './App.css'

const API_BASE = 'http://localhost:8000'

function App() {
  const [prompt, setPrompt] = useState('')
  const [messages, setMessages] = useState([]) // {role: 'user' | 'bot', text: string}
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const messagesEndRef = useRef(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

    // 🔹 ЗАГРУЗКА ИСТОРИИ ПРИ МОНТАЖЕ
  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const res = await fetch(`${API_BASE}/requests`)
        if (!res.ok) {
          throw new Error(`Ошибка получения истории: ${res.status}`)
        }

        const data = await res.json()
        // Ожидаем, что backend возвращает:
        // [
        //   { id, ip_address, prompt, response },
        //   ...
        // ]

        const historyMessages = data.flatMap((item) => {
          const arr = []
          if (item.prompt) {
            arr.push({ role: 'user', text: item.prompt })
          }
          if (item.response) {
            arr.push({ role: 'bot', text: item.response })
          }
          return arr
        })

        setMessages(historyMessages)
      } catch (e) {
        console.error(e)
        setError(e.message || 'Не удалось загрузить историю')
      }
    }

    fetchHistory()
  }, [])

  const handleSend = async () => {
    if (!prompt.trim() || loading) return

    const userMessage = { role: 'user', text: prompt.trim() }
    setMessages((prev) => [...prev, userMessage])
    setPrompt('')
    setError('')
    setLoading(true)

    try {
      const response = await fetch(`${API_BASE}/requests`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ prompt: userMessage.text })
      })

      if (!response.ok) {
        throw new Error(`Ошибка сервера: ${response.status}`)
      }

      const data = await response.json()
      // У тебя в main.py: return {"answer": {answer}}
      // Это означает, что answer приходит как множество, вытащим первую строку
      let answerText = ''
      if (data && data.answer) {
        const values = Array.from(data.answer)
        answerText = values[0] ?? ''
      }

      const botMessage = {
        role: 'bot',
        text: answerText || 'Пустой ответ от сервера'
      }

      setMessages((prev) => [...prev, botMessage])
    } catch (e) {
      console.error(e)
      setError(e.message || 'Неизвестная ошибка')
    } finally {
      setLoading(false)
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="app">
      <div className="chat-container">
        <header className="chat-header">
          <h1>Чат с api OpenAI</h1>
          <span className="chat-subtitle">FastAPI + React + OpenAI</span>
        </header>

        <div className="chat-messages">
          {messages.length === 0 && (
            <div className="chat-empty">
              Напиши что‑нибудь, чтобы начать диалог с ботом.
            </div>
          )}
          {messages.map((m, idx) => (
            <div
              key={idx}
              className={`message-row ${m.role === 'user' ? 'message-user' : 'message-bot'}`}
            >
              <div className="message-avatar">
                {m.role === 'user' ? '👤' : '🤖'}
              </div>
              <div className="message-bubble">
                {m.text}
              </div>
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>

        {error && <div className="error-banner">{error}</div>}

        <div className="chat-input-area">
          <textarea
            className="chat-input"
            placeholder="Введите ваш prompt и нажмите Enter (Shift+Enter — новая строка)..."
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            onKeyDown={handleKeyDown}
            rows={3}
          />
          <button
            className="send-button"
            onClick={handleSend}
            disabled={loading || !prompt.trim()}
          >
            {loading ? 'Отправка...' : 'Отправить'}
          </button>
        </div>
      </div>
    </div>
  )
}

export default App

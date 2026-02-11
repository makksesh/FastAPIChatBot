from openai import OpenAI
from config import config_obj

client = OpenAI(
    api_key=config_obj.gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

def get_answer_from_prompt(prompt: str):
    resp = client.chat.completions.create(
        model="models/gemini-2.5-flash",
        messages=[{"role": "user", "content": prompt}],
    )
    # ЗАЩИТА:
    # 1. Берем первый вариант (choices[0])
    # 2. Берем сообщение
    # 3. Берем контент.
    # НО! Иногда нейросеть может вернуть None (редко, но бывает).
    # Конструкция `or ""` превратит None в пустую строку, чтобы не сломать фронтенд.
    return resp.choices[0].message.content or ""
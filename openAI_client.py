from openai import OpenAI
from config import config_obj

client = OpenAI(
    api_key=config_obj.openAI_api_key,
    base_url="https://api.perplexity.ai",
)

def get_answer_from_prompt(prompt: str):
    resp = client.chat.completions.create(
        model="sonar",
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.choices[0].message.content
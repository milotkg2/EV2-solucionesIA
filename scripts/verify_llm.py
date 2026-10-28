import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise RuntimeError("GROQ_API_KEY no está configurada en .env")

client = Groq(api_key=api_key)
response = client.chat.completions.create(
    model=os.getenv("GROQ_MODELO", "openai/gpt-oss-120b"),
    messages=[{"role": "user", "content": "Responde solo: OK"}],
    max_completion_tokens=8,
)
print(response.choices[0].message.content)

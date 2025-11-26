import os 
from typing import List 
from openai import OpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

EMBEDDING_MODEL ="text-embedding-3-small"
CHAT_MODEL = "04-mini"

def embed_texts(texts: list[str])-> list[list[float]]:
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=texts 
    )
    return [d.embedding for d in response.data]

def chat_with_context(system_prompt:str,context:str,messages:list[dict])->str:
    full_messages = [
        {"role":"system","content":system_prompt},
        {
            "role":'system',
            "content":(
                "Here is some context from Damian's portofolio:\n\n"+ context
            )
        },
        *messages
    ]

    resp = client.chat.completions.create(
        model = CHAT_MODEL,
        messages = full_messages,
        temperature=0.3
    )
    return resp.choices[0].message.content or ""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional,List,Dict,Any 
import httpx 
from rag.rag_types import Provider
import os 

@dataclass 
class LLMConfig:
    openai_api_key: Optional[str] = None
    openai_model: str = os.getenv("CHAT_MODEL")
    ollama_url: str =  os.getenv("OLLAMA_URL", "http://localhost:11434")
    ollama_model: str = os.getenv("OLLAMA_MODEL")
    timeout_s:float=45.0

class LLMClient:
    def __init__(self,cfg:LLMConfig):
        self.cfg = cfg
    
    async def generate(
            self,
            system:str,
            user:str,
            provider_preference:List[Provider] = ["ollama", "openai"],
            temperature:float=0.7,
    )-> str:
        last_err: Optional[str] = None

        for provider in provider_preference:
            try:
                if provider == "ollama":
                    return await self._generate_ollama(system, user, temperature)
                elif provider == "openai":
                    if not self.cfg.openai_api_key:
                        raise RuntimeError("OpenAI API key not configured")
                    return await self._generate_openai(system, user, temperature)
            except Exception as e:
                last_err = f"{provider} error: {repr(e)}"
                continue
        raise RuntimeError(f"All LLM providers failed. Last error: {last_err}")

    async def _openai_chat(self, system:str, user:str, temperature:float) -> str:
        url  = "https://api.openai.com/v1/chat/completions"
        headers ={
            "Authorization": f"Bearer {self.cfg.openai_api_key}",
            "Content-Type": "application/json"
        }
        payload: Dict[str,Any] = {
            "model": self.cfg.openai_model,
            "messages":[
                {"role":"system", "content": system},
                {"role":"user", "content": user}
            ],
            "temperature": temperature,
        }
        
        async with httpx.AsyncClient(timeout=self.cfg.timeout_s) as client:
            resp = await client.post(url, headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"].strip()
    
    async def _ollama_chat(self,system:str,user:str,temperature:float)-> str:
        url = f"{self.cfg.ollama_url}/api/chat"
        payload = {
            "model": self.cfg.ollama_model,
            "messages":[
                {"role":"system", "content": system},
                {"role":"user", "content": user}
            ],
            "temperature": temperature,
        }
        async with httpx.AsyncClient(timeout=self.cfg.timeout_s) as client:
            resp = await client.post(url, json=payload)
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"].strip()
from openai import AsyncOpenAI, APIError
from core.logger import app_logger

class AIManager:
    def __init__(self, api_key: str, base_url: str = "https://api.proxyapi.ru/openai/v1") -> None:
        self._client = AsyncOpenAI(
            api_key=api_key,
            base_url=base_url
        )
    
    async def chat_response(self, message: str, model: str, system_instruction: str, temperature: float, max_tokens: int) -> str:
        full_message = [{"role": "system", "content": system_instruction}, {"role": "user", "content": message}]

        try:
            response = await self._client.chat.completions.create(
                model=model,
                messages=full_message,
                temperature=temperature,
                max_tokens=max_tokens
            )

            return response.choices[0].message.content
        
        except APIError as e:
            app_logger.error(f"ProxyAPI Error. Chat response: {e}")
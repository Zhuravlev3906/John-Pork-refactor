import os
import io
import base64
import aiofiles
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
    
    async def edit_image(self, user_prompt: str, system_instruction: str, model: str, size: str, quality: str, reference_image: str = "assets/pig.jpg"):
        if not os.path.exists(reference_image):
            app_logger.error(f"File {reference_image} not exists.")

        prompt = (
            f"{system_instruction}"
            f"{user_prompt}"
        )

        try:
            async with aiofiles.open(reference_image, "rb") as f:
                ref_img_bytes = await f.read()

            response = await self._client.images.edit(
                model=model,
                image=ref_img_bytes,
                prompt=prompt,
                size=size,
                quality=quality
            )

            return base64.b64decode(response.data[0].b64_json)

        except APIError as e:
            app_logger.error(f"ProxyAPI Error. Edit image: {e}")
        except Exception as e:
            app_logger.error(f"Error reading file or processing image: {e}")
    
    async def face_swap(self, human_face: bytes, system_instruction: str, model: str, size: str, quality: str, reference_image: str = "assets/pig.jpg"):
        try:
            async with aiofiles.open(reference_image, "rb") as f:
                ref_img_bytes = await f.read()
            
            ref_img_io = io.BytesIO(ref_img_bytes)
            ref_img_io.name = os.path.basename(reference_image)

            human_image = io.BytesIO(human_face)
            human_image.name = "human.jpg"

            response = await self._client.images.edit(
                model=model,
                image=[ref_img_io, human_image],
                prompt=system_instruction,
                size=size,
                quality=quality
            )

            return base64.b64decode(response.data[0].b64_json)

        except APIError as e:
            app_logger.error(f"ProxyAPI Error. Face swap: {e}")
        except Exception as e:
            app_logger.error(f"Error reading file or processing face swap: {e}")
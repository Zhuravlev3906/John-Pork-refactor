from typing import Optional

from sqlalchemy import select
from sqlalchemy.dialects.sqlite import insert

from core.database import get_session, User
from core.logger import logger

async def set_user_language(user_id: int, language_code: str) -> None:
    normalized_lang = language_code.lower()[:2]
    
    async with get_session() as session:
        stmt = insert(User).values(user_id=user_id, language=normalized_lang)
        
        stmt = stmt.on_conflict_do_update(
            index_elements=['user_id'],
            set_=dict(language=normalized_lang)
        )
        
        await session.execute(stmt)
        logger.info(f"User {user_id} language set to '{normalized_lang}'")

async def get_user_language(user_id: int, default_lang: Optional[str] = "en") -> str:
    async with get_session() as session:
        stmt = select(User.language).where(User.user_id == user_id)
        result = await session.execute(stmt)
        lang = result.scalar_one_or_none()

        if lang:
            return lang
        
        fallback = default_lang.lower()[:2] if default_lang else "en"
        return fallback
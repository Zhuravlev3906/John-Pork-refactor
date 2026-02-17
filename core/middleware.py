from telegram import Update
from telegram.ext import ContextTypes

from core.lang_manager import LangManager
from core.user_service import get_user_language

lang_manager = LangManager("lang.yaml")

async def set_language_context(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id if update.effective_user else None
    tg_lang = update.effective_user.language_code if update.effective_user else "en"

    if user_id:
        lang_code = await get_user_language(user_id, tg_lang)
    else:
        lang_code = tg_lang or "en"

    context.lang = getattr(lang_manager, lang_code, lang_manager.en)
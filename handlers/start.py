from pathlib import Path

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ChatType
from telegram.ext import ContextTypes

from core.config_manager import Config
from core.lang_manager import RuYamlLangModel
from core.logger import logger

config = Config()

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    
    if chat.type != ChatType.PRIVATE:
        return

    try:
        lang_model = context.lang

        lang_code = "ru" if isinstance(lang_model, RuYamlLangModel) else "en"

        keyboard = [
            [
                InlineKeyboardButton(
                    text=lang_model.btn_main_group,
                    url=config.bot.main_group_url
                )
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        image_path = Path(f"assets/start_banner_{lang_code}.png")
        
        if image_path.exists():
            with image_path.open("rb") as photo:
                await context.bot.send_photo(
                    chat_id=chat.id,
                    photo=photo,
                    caption=lang_model.start,
                    reply_markup=reply_markup
                )
        else:
            logger.warning(f"Start banner not found at {image_path}")
            await context.bot.send_message(
                chat_id=chat.id,
                text=lang_model.start,
                reply_markup=reply_markup
            )

    except Exception as e:
        logger.error(f"Error in start_command: {e}")
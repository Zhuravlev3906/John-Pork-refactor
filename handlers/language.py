from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ChatType
from telegram.ext import ContextTypes
from telegram.error import TelegramError

from core.lang_manager import LangManager
from core.user_service import set_user_language, get_user_language
from core.logger import logger

lang_manager = LangManager("lang.yaml")

async def send_lang_menu(user_id: int, context: ContextTypes.DEFAULT_TYPE, chat_id: int = None):
    current_lang_code = await get_user_language(user_id, "en")
    lang_model = getattr(lang_manager, current_lang_code, lang_manager.en)

    keyboard = [
        [
            InlineKeyboardButton(lang_model.btn_ru, callback_data="set_lang_ru"),
            InlineKeyboardButton(lang_model.btn_en, callback_data="set_lang_en")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    target_chat_id = chat_id if chat_id else user_id
    await context.bot.send_message(
        chat_id=target_chat_id,
        text=lang_model.menu_choose_language,
        reply_markup=reply_markup
    )

async def lang_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    
    if not user:
        return

    try:
        if chat.type == ChatType.PRIVATE:
            await send_lang_menu(user.id, context, chat.id)
        else:
            try:
                await send_lang_menu(user.id, context)
            except TelegramError:
                await update.message.reply_text(context.lang.error_private_needed)
    except Exception as e:
        logger.error(f"Error in lang_command: {e}")

async def lang_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = update.effective_user
    
    if not query.data or not query.data.startswith("set_lang_"):
        await query.answer()
        return

    new_lang_code = query.data.split("_")[-1]

    try:
        await set_user_language(user.id, new_lang_code)
        
        # Получаем модель нового языка для ответа об успехе
        new_lang_model = getattr(lang_manager, new_lang_code, lang_manager.en)
        
        await query.edit_message_text(
            text=new_lang_model.lang_set_success
        )
        
    except Exception as e:
        logger.error(f"Error setting language for user {user.id}: {e}")
        await query.answer(context.lang.error_change_lang, show_alert=True)
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler
from telegram.constants import ChatType

from core.lang_manager import RuYamlLangModel, EnYamlLangModel

async def lucky_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang: RuYamlLangModel | EnYamlLangModel = getattr(context, "lang", None)
    
    if update.effective_chat.type != ChatType.PRIVATE:
        await update.message.reply_text(lang.error_private_needed if lang else "Use private chat.")
        return

    # Генерируем выигрышный индекс от 0 до 9
    winning_index = random.randint(0, 9)
    
    keyboard = []
    row = []
    for i in range(10):
        # callback_data будет содержать "lucky:{index}:{is_win}"
        is_win = 1 if i == winning_index else 0
        button = InlineKeyboardButton(
            text=lang.lucky_btn.format(i=i+1),
            callback_data=f"lucky:{i}:{is_win}"
        )
        row.append(button)
        if len(row) == 2:
            keyboard.append(row)
            row = []
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(lang.lucky_start, reply_markup=reply_markup)

async def lucky_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    data = query.data.split(":")
    is_win = int(data[2])
    
    lang: RuYamlLangModel | EnYamlLangModel = getattr(context, "lang", None)
    
    if is_win:
        text = lang.lucky_win
    else:
        text = lang.lucky_loss
        
    await query.edit_message_text(text=text)

def get_lucky_handlers():
    return [
        CommandHandler("lucky", lucky_command),
        CallbackQueryHandler(lucky_callback, pattern="^lucky:")
    ]

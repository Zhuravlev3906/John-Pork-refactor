from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes

from core.config_manager import Config
from core.logger import logger
from utils.ai_function import AIManager
from utils.chat_address import BotAddressDetector

async def chat_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.text:
        return

    config = Config()
    
    bot_user = await context.bot.get_me()
    bot_username = bot_user.username
    chat_type = update.message.chat.type
    text = update.message.text

    is_addressed = False

    if chat_type == "private":
        is_addressed = True
    else:
        is_reply_to_bot = (
            update.message.reply_to_message 
            and update.message.reply_to_message.from_user.id == bot_user.id
        )
        has_mention = f"@{bot_username}" in text
        
        if is_reply_to_bot or has_mention:
            is_addressed = True
        else:
            detector = BotAddressDetector(keywords=config.bot.address_keywords)
            if detector.is_addressing(text):
                is_addressed = True

    if not is_addressed:
        return

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)

    ai_manager = AIManager(api_key=config.proxy_api_key)

    try:
        response = await ai_manager.chat_response(
            message=text,
            model=config.ai.chat_model,
            system_instruction=config.ai.chat_system_prompt,
            temperature=config.ai.temperature,
            max_tokens=config.ai.max_tokens
        )
        
        if response:
            await update.message.reply_text(response)
            
    except Exception as e:
        logger.error(f"Error in chat_message_handler: {e}")
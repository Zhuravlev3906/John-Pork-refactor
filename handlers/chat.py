import random

from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes

from core.config_manager import Config
from core.logger import logger
from utils.ai_function import AIManager
from utils.chat_address import BotAddressDetector
from utils.cooldown import cooldown_manager

async def chat_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.text:
        return

    config = Config()
    
    bot_user = await context.bot.get_me()
    bot_username = bot_user.username
    chat_type = update.message.chat.type
    text = update.message.text
    chat_id = update.effective_chat.id

    is_addressed = False

    if chat_type == "private":
        return
    
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

    system_prompt = config.ai.chat_system_prompt

    if not is_addressed:
        if len(text.split()) < 3:
            return

        text_lower = text.lower()
        
        has_finance = any(trigger in text_lower for trigger in config.bot.eavesdrop_finance_triggers)
        has_aggression = any(trigger in text_lower for trigger in config.bot.eavesdrop_aggression_triggers)
        
        should_eavesdrop = False
        
        if has_finance:
            should_eavesdrop = True
        elif has_aggression and random.randint(1, 100) <= 40:
            should_eavesdrop = True
        elif random.randint(1, 100) <= config.bot.eavesdrop_chance:
            should_eavesdrop = True

        if not should_eavesdrop:
            return
            
        if not cooldown_manager.check_and_set(chat_id, config.bot.eavesdrop_cooldown):
            return
            
        system_prompt = config.ai.eavesdrop_system_prompt

    await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

    ai_manager = AIManager(api_key=config.proxy_api_key)

    try:
        response = await ai_manager.chat_response(
            message=text,
            model=config.ai.chat_model,
            system_instruction=system_prompt,
            temperature=config.ai.temperature,
            max_tokens=config.ai.max_tokens
        )
        
        if response:
            await update.message.reply_text(response)
            
    except Exception as e:
        logger.error(f"Error in chat_message_handler: {e}")
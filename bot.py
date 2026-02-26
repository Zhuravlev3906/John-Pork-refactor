import sys
import asyncio

from telegram import Update
from telegram.ext import (
    Application,
    ApplicationBuilder, 
    CommandHandler, 
    CallbackQueryHandler, 
    MessageHandler,
    TypeHandler,
    filters
)
from loguru import logger

from core.config_manager import Config
from core.database import init_db
from core.middleware import set_language_context
from handlers.language import lang_command, lang_callback
from handlers.start import start_command
from handlers.chat import chat_message_handler

async def post_init(application: Application) -> None:
    await init_db()
    logger.info("Post-init actions completed.")

def main() -> None:
    logger.info("Starting Bot...")

    config = Config()
    
    if not config.telegram_bot_token:
        logger.critical("Bot token not found in configuration!")
        sys.exit(1)

    application = (
        ApplicationBuilder()
        .token(config.telegram_bot_token)
        .post_init(post_init)
        .build()
    )

    application.add_handler(TypeHandler(Update, set_language_context), group=-1)

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("lang", lang_command))
    application.add_handler(CallbackQueryHandler(lang_callback, pattern="^set_lang_"))
    
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_message_handler))

    logger.info("Bot is running polling...")
    
    application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    try:
        if sys.platform == 'win32':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
            
        main()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.critical(f"Fatal error: {e}")
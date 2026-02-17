import sys
import asyncio

from telegram import Update
from telegram.ext import (
    Application,
    ApplicationBuilder, 
    CommandHandler, 
    CallbackQueryHandler, 
    TypeHandler
)
from loguru import logger

from core.config_manager import Config
from core.database import init_db
from core.middleware import set_language_context
from handlers.language import lang_command, lang_callback

async def post_init(application: Application) -> None:
    await init_db()
    logger.info("Post-init actions completed.")

def main():
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

    application.add_handler(CommandHandler("lang", lang_command))
    application.add_handler(CallbackQueryHandler(lang_callback, pattern="^set_lang_"))

    logger.info("Bot is running polling...")
    
    application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    try:            
        main()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.critical(f"Fatal error: {e}")
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes, ConversationHandler

from core.config_manager import Config
from core.lang_manager import LangManager
from core.logger import logger
from utils.ai_function import AIManager

WAIT_PHOTO = 1

async def porkify_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    lang_code = context.user_data.get("language", "en")
    lang_manager = LangManager()
    texts = getattr(lang_manager, lang_code)
    
    reply_msg = update.message.reply_to_message
    if reply_msg and reply_msg.photo:
        photo_file_id = reply_msg.photo[-1].file_id
        await _process_and_send_porkify(update, context, photo_file_id)
        return ConversationHandler.END

    await update.message.reply_text(texts.swap_face_start)
    return WAIT_PHOTO


async def porkify_receive_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if not update.message.photo:
        return WAIT_PHOTO
        
    photo_file_id = update.message.photo[-1].file_id
    await _process_and_send_porkify(update, context, photo_file_id)
    
    return ConversationHandler.END


async def porkify_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    lang_code = context.user_data.get("language", "en")
    lang_manager = LangManager()
    texts = getattr(lang_manager, lang_code)
    
    await update.message.reply_text(texts.swap_face_cancel)
    return ConversationHandler.END


async def _process_and_send_porkify(update: Update, context: ContextTypes.DEFAULT_TYPE, file_id: str) -> None:
    lang_code = context.user_data.get("language", "en")
    lang_manager = LangManager()
    texts = getattr(lang_manager, lang_code)
    chat_id = update.effective_chat.id
    
    status_msg = await update.message.reply_text(texts.swap_face_process)
    await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.UPLOAD_PHOTO)

    config = Config()
    ai_manager = AIManager(api_key=config.proxy_api_key)

    try:
        file = await context.bot.get_file(file_id)
        image_bytes = await file.download_as_bytearray()
        
        result_image_bytes = await ai_manager.face_swap(
            human_face=bytes(image_bytes),
            system_instruction=config.ai.face_swap_system_prompt,
            model=config.ai.image_model,
            size=config.ai.image_size,
            quality=config.ai.quality,
            reference_image=config.ai.reference_image
        )
        
        if result_image_bytes:
            await context.bot.send_photo(
                chat_id=chat_id, 
                photo=result_image_bytes, 
                reply_to_message_id=update.message.message_id,
                caption=texts.swap_face_done
            )
        else:
            await update.message.reply_text(texts.swap_face_error)
            
    except Exception as e:
        logger.error(f"Error in porkify processing: {e}")
        await update.message.reply_text(texts.swap_face_error)
    finally:
        await status_msg.delete()
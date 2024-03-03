import logging, handlers, os
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ConversationHandler
from dotenv import load_dotenv

load_dotenv()
TELEGRAM_API_KEY = os.getenv('TELEGRAM_API_KEY')


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logging.getLogger('httpx').setLevel(logging.WARNING) # Logging only important things.


if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_API_KEY).build()
    
    timezone_handler = ConversationHandler(
        entry_points=[CommandHandler('start', handlers.start)],
        states={handlers.SELECT_TIMEZONE: [MessageHandler(filters.TEXT, handlers.select_timezone)]},
        fallbacks=[],
        allow_reentry=True # Allows to "reset" the conversation if the user resends "/start"
    )
    set_handler = CommandHandler('set', handlers.set_time)
    unset_handler = CommandHandler('unset', handlers.unset)
    quote_handler = CommandHandler('quote', handlers.loose_quote)
    help_handler = CommandHandler('help', handlers.help)
    unknown_handler = MessageHandler(filters.COMMAND, handlers.unknown)

    application.add_handlers([timezone_handler, set_handler, unset_handler, quote_handler, help_handler])
    application.add_handler(unknown_handler) # this must be the last handler, it works as a fallback.

    try:
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    except Exception as e:
        logging.error(f'ERROR: {e}')
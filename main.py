from config import api_token
import logging
import handlers
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ConversationHandler
token = api_token


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logging.getLogger('httpx').setLevel(logging.WARNING) # Logging only important things.


if __name__ == '__main__':
    application = ApplicationBuilder().token(token).build()
    
    timezone_handler = ConversationHandler(
        entry_points=[CommandHandler('start', handlers.start)],
        states={handlers.SELECT_TIMEZONE: [MessageHandler(filters.TEXT, handlers.select_timezone)]},
        fallbacks=[],
        allow_reentry=True # Allows to "reset" the conversation if the user resends "/start"
    )
    set_handler = CommandHandler('set', handlers.set_time)
    unset_handler = CommandHandler('unset', handlers.unset)
    unknown_handler = MessageHandler(filters.COMMAND, handlers.unknown)

    application.add_handler(timezone_handler)
    application.add_handler(set_handler)
    application.add_handler(unset_handler)
    application.add_handler(unknown_handler) # this must be the last handler, works as a fallback.
    application.run_polling(allowed_updates=Update.ALL_TYPES)


    # Even though all timezones are working correctly, the bot isn't sending the message in the scheduled time, MUST CHECK IT!
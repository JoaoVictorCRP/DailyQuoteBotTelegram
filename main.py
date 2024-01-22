from config import api_token
import logging
import handlers
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler
token = api_token


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logging.getLogger('httpx').setLevel(logging.WARNING) # Logar somente coisas importantes


if __name__ == '__main__':
    application = ApplicationBuilder().token(token).build()
    
    quote_handler = CommandHandler('quote', handlers.quote)
    start_handler = CommandHandler(['start','help'], handlers.start)
    set_handler = CommandHandler('set', handlers.set_time)
    unset_handler = CommandHandler('unset', handlers.unset)
    unknown_handler = MessageHandler(filters.COMMAND, handlers.unknown)

    application.add_handler(start_handler)
    application.add_handler(set_handler)
    application.add_handler(unset_handler)
    application.add_handler(quote_handler)
    application.add_handler(unknown_handler) # Esse handler deve ficar sempre por último, como se fosse um ELSE de comandos, já que ele é disparado por qualquer "/" que tiver

    application.run_polling(allowed_updates=Update.ALL_TYPES)
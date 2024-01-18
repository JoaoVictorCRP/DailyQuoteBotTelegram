from config import api_token
import logging
import handlers
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler
# from telegram import Update
# from telegram.ext import filters, MessageHandler, ApplicationBuilder, ContextTypes, CommandHandler
token = api_token


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


if __name__ == '__main__':
    application = ApplicationBuilder().token(token).build()
    
    start_handler = CommandHandler('start', handlers.start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handlers.echo)
    fala_handler = CommandHandler('fala', handlers.quote)
    unknown_handler = MessageHandler(filters.COMMAND, handlers.unknown)

    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    application.add_handler(fala_handler)
    application.add_handler(unknown_handler) # Esse handler deve ficar sempre por último, como se fosse um ELSE de comandos, já que ele é disparado por qualquer "/" que tiver

    application.run_polling()
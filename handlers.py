from telegram import Update
from telegram.ext import ContextTypes
from datetime import time
import utils.requisiton as rq
import pytz

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Starting command, the bot explains its funtionality."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
          text="Hi! Thanks for subscribing to Quoach BOT. \n\nUse /set to define the hour of the day in which you want to receive a motivational quote."
    )

async def quote(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends the quote to the user."""
    job = context.job
    content = await rq.get_random_quote()
    statement = content[0]
    thinker = content[1]
    await context.bot.send_message(
        job.chat_id,
        text=f'"{statement}"\n\n- {thinker}'
    )

def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Remove job with given name. Return whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal() # Removing each job.
    return True

async def set_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Add daily job to the queue."""
    chat_id = update.effective_message.chat_id

    # print(f'\n\nArgs 0 aqui: {context.args[0]}\n\n') # Testing
    try:
        #args[0] contains the timer setted by the user.
        chosen_time = context.args[0]
        chosen_time = chosen_time.split(':')
        hours = int(chosen_time[0])
        minutes = int(chosen_time[1].zfill(2)) #zfill adds zero on the left case < 10.

        if hours>24 or hours<0:
            await update.effective_message.reply_text("Please, enter a valid positive value for hours.")
            return
        if minutes>59 or minutes<0:
            await update.effective_message.reply_text("Please, enter a valid positive value for minutes.")
        
        job_removed = remove_job_if_exists(str(chat_id), context)

        tz_brazil = pytz.timezone('America/Sao_Paulo')

        context.job_queue.run_daily(quote, time=time(hour=hours, minute=minutes, tzinfo=tz_brazil), chat_id=chat_id, name=str(chat_id)) 

        text= f'Daily motivational quote scheduled for {hours}:{minutes} in the Brazilian timezone.'
        if job_removed:
            text += "Old one was removed!"
        await update.effective_message.reply_text(text)
    
    except(IndexError, ValueError):
        await update.effective_message.reply_text("Usage: /set <hrs>:<mins>")

async def unset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Remove the job if the user changed their mind."""
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Daily quote successfully removed!' if job_removed else "You don't have any setted jobs."
    await update.message.reply_text(text)
    
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text= f'"{update.message.text}" is not a valid command.'
    )
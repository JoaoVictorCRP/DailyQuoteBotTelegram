from telegram import Update
from telegram.ext import ContextTypes,CallbackContext, ConversationHandler
from datetime import time, datetime
import utils.requisiton as rq
import pytz, re
from time import sleep

SELECT_TIMEZONE = 1


async def start(update: Update, context: CallbackContext) -> int:
    """Starting command, the bot explains its funtionality."""
    user = update.effective_user

    await update.message.reply_text(f'Hello {user.first_name}, Thank you for subscribing to Quoach BOT.')
    with open('images/utc_map.png', 'rb') as timezone_map:
        await update.message.reply_photo(timezone_map, caption="Timezone Map")

    await update.message.reply_text(
        "First things first, let's select your timezone.\nUse the Timezone Map above to view your location's timezone.",
    ) 

    return SELECT_TIMEZONE

async def select_timezone(update: Update, context: CallbackContext) -> int:
    """Handle selected timezone."""
    user_timezone = update.message.text

    # misplaced_signal = re.search('[+-]', user_timezone) # if user inputs "3+", for example.
    # if misplaced_signal:
    #     print(f'entering conditional, value is {user_timezone}')
    #     user_timezone = f'{misplaced_signal[0]}{user_timezone[:1]}' #replacing the order
    #     print(f'leaving conditional, value is {user_timezone}')
    
    timezone_validation = re.search(r'[+-]?\d{1,2}',user_timezone)
    if (timezone_validation is None):
        print(f'{timezone_validation}, input was: {user_timezone}')
        await update.message.reply_text('Please, insert a valid UTC timezone.')
        return
    
    user_timezone = timezone_validation[0]

    if int(user_timezone) < -11 or int(user_timezone) > 14:
        await update.message.reply_text('Sorry, timezone must be between -11 and +14')
        return
    
    print(f'user tz value: {user_timezone}')
    context.user_data['timezone'] = f'Etc/GMT{(user_timezone)}'
    await update.message.reply_text(
        f'Great choice! Your timezone is now set to UTC{user_timezone}.\nYou may now use /set to define the moment of your daily message.'
    )

    return ConversationHandler.END

async def quote(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends random quote to the user."""
    job = context.job
    content = await rq.get_random_quote()
    statement = content[0]
    thinker = content[1]
    await context.bot.send_message(
        job.chat_id,
        text=f'"{statement}"\n\n- {thinker}'
    )

async def loose_quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Random quote sender, not related to schedule."""
    try:
        if context.args: # If args where passed...
            content = await rq.get_random_quote(context.args[0])
        else:
            print('else was hitted') 
            content = await rq.get_random_quote()
        statement = content[0]
        thinker = content[1]
        await context.bot.send_message(
            update.effective_chat.id,
            text=f'"{statement}"\n\n- {thinker}'
        )
    except:
        await context.bot.send_message(
            update.effective_chat.id,
            text=f'Please, select a valid quote theme!'
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
    if 'timezone' not in context.user_data:
        await update.effective_message.reply_text('Please use /start to set your timezone first')
        return
    
    try:
        #args[0] contains the timer setted by the user.
        chosen_time = context.args[0]
        chosen_time = chosen_time.split(':')
        hours = int(chosen_time[0])
        minutes = int(chosen_time[1]) #zfill adds zero on the left case < 10.

        if hours>24 or hours<0:
            await update.effective_message.reply_text("Please, enter a valid positive value for hours.")
            return
        if minutes>59 or minutes<0:
            await update.effective_message.reply_text("Please, enter a valid positive value for minutes.")
        
        job_removed = remove_job_if_exists(str(chat_id), context)
        tz = pytz.timezone(context.user_data['timezone'])
        
        # Debugging purpose:
        now_in_tz = datetime.now(tz)
        print(f"Current time in {tz}: {now_in_tz.strftime('%Y-%m-%d %H:%M:%S')}")


        context.job_queue.run_daily(quote, time=time(hour=hours, minute=minutes, tzinfo=tz), chat_id=chat_id, name=str(chat_id)) 

        text= f'Daily motivational quote scheduled for {hours}:{str(minutes).zfill(2)} in the {tz} timezone.'
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
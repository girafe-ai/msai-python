import random
import threading
import time
import sched
from datetime import datetime

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters


deadlines = [
    {'ha_name': 'ha #1', 'deadline': datetime(year=2021, month=12, day=29, hour=21)},
    {'ha_name': 'ha #2', 'deadline': datetime(year=2021, month=12, day=29, hour=21)},
]
users = {
    # '12312': {'first_name': '132', ..., 'msai_student': True},
}


#
# Bot methods
#

def remember_user(user):
    if user.id in users:
        return

    users[user.id] = {
        'is_bot': user.is_bot,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'username': user.username,
        'msai_student': True
    }


def hello(update: Update, context: CallbackContext) -> None:
    remember_user(update.effective_user)
    update.message.reply_text(f'Hello {update.effective_user.first_name}')


def random_command(update: Update, context: CallbackContext) -> None:
    """/random 1 10"""
    remember_user(update.effective_user)
    try:
        _, min_number, max_number = update.message.text.split(' ')
        min_number = int(min_number)
        max_number = int(max_number)
    except:
        min_number, max_number = 1, 10

    update.message.reply_text(f'Answer: {random.randint(min_number, max_number)}')


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    remember_user(update.effective_user)
    update.message.reply_text(update.message.text)


updater = Updater('5067953145:AAG4bSExQ6sbOf6OhH2nFhxGLaAvblzZ0VE')
updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(CommandHandler('random', random_command))
updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))


#
# Scheduler code
#

scheduler = sched.scheduler(time.time, time.sleep)


def send_notification(deadline):
    for user_id, user_data in users.items():
        print(user_id, user_data)
        if user_data['msai_student']:
            updater.bot.send_message(user_id, f'{deadline["ha_name"]} deadline is {deadline["deadline"]}')


def run_scheduler():
    for deadline in deadlines:
        print(deadline)
        timestamp = deadline['deadline'].timestamp()
        notification_periods = [24 * 3600, 3600, 60]
        now = time.time()
        for period in notification_periods:
            if timestamp - period > now:
                scheduler.enterabs(timestamp - period, 1, send_notification, argument=(deadline,))

        # for debug
        # scheduler.enterabs(now + 5, 1, send_notification, argument=(deadline,))

    scheduler.run()


# start scheduler in separate thread
t = threading.Thread(target=run_scheduler)
t.start()

# start bot in main thread
updater.start_polling()
updater.idle()

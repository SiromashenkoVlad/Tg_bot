# Импортируем необходимые классы.
import logging
from telegram.ext import Application, MessageHandler, filters
from config import BOT_TOKEN
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove

# Запускаем логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


async def close_keyboard(update, context):
    await update.message.reply_text(
        "Ok",
        reply_markup=ReplyKeyboardRemove()
    )


# Напишем соответствующие функции.
async def help(update, context):
    await update.message.reply_text(
        "Я бот справочник.")


async def start(update, context):
    await update.message.reply_text(
        "Я бот-справочник. Какая информация вам нужна?",
        reply_markup=markup
    )


async def register(update, context):
    pass


async def auth(update, context):
    pass


async def all_hours(update, context):
    pass


async def charts(update, context):
    pass


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("register", register))
    application.add_handler(CommandHandler("auth", auth))
    application.add_handler(CommandHandler("all_hours", all_hours))
    application.add_handler(CommandHandler("charts", charts))

    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("close", close_keyboard))
    application.add_handler(CommandHandler("start", start))
    application.run_polling()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    reply_keyboard = [['/register', '/auth'],
                      ['/all_hours', '/charts']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    main()

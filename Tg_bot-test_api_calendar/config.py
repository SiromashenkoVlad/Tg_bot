BOT_TOKEN = '7705829796:AAHCPak3HGEz-HOYg36PejMT2GvQmdhYo1Q'

HELP_COMMAND_TEXT = """
 Список команд:
 /start - начать использовать бота (также старт позволяет "перезагрузить" бота в слечае ошибки)
 /help - вывести список команд
 /graph - показать статистику в виде диаграмы
 /recent - показать ваше последнее событие
 """

START_COMMAND_TEXT = """Я - бот-справочник! Я могу помочь тебе структурировать
 расписание в приложении Google Calendar. Какая информация тебе нужна?"""

# Цвета календаря (стандартные цвета Google Calendar)
COLOR_MAP = {
    '1': {'name': 'Lavender', 'hex': '#7986cb'},
    '2': {'name': 'Sage', 'hex': '#33b679'},
    '3': {'name': 'Grape', 'hex': '#8e24aa'},
    '4': {'name': 'Flamingo', 'hex': '#e67c73'},
    '5': {'name': 'Banana', 'hex': '#f6c026'},
    '6': {'name': 'Tangerine', 'hex': '#f5511d'},
    '7': {'name': 'Peacock', 'hex': '#039be5'},
    '8': {'name': 'Graphite', 'hex': '#616161'},
    '9': {'name': 'Blueberry', 'hex': '#3f51b5'},
    '10': {'name': 'Basil', 'hex': '#0b8043'},
    '11': {'name': 'Tomato', 'hex': '#d60000'},
}

# Настройки доступа
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'token.pickle'

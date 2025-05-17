from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Помощь!')],
                                     [KeyboardButton(text='Моя статистика')],
                                     [KeyboardButton(text='Последнее событие')],
                                     [KeyboardButton(text='Стоп')]],
                           resize_keyboard=True,
                           input_field_placeholder='Выберите пункт меню:')

chose_type = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Старт!')],
              [KeyboardButton(text='По локации')],
              [KeyboardButton(text='По цвету')],
              [KeyboardButton(text='Стоп')]],
    resize_keyboard=True,
    input_field_placeholder='Выберите пункт меню:'
)

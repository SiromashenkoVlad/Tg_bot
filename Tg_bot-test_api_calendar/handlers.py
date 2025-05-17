import asyncio
from aiogram import F, types, Router
from aiogram.filters import CommandStart, Command
import config
from google_api import authenticate_google_calendar, build, get_all_user_events, print_events, save_to_csv
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.chat_action import ChatActionSender
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram.types import FSInputFile

import kb

# Библиотеки для составления диаграм
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set()

router = Router()

creds = authenticate_google_calendar()
service = build('calendar', 'v3', credentials=creds)
events = get_all_user_events(service)
save_to_csv(events)


@router.message(Command('start'))
@router.message(F.text == 'Старт!')  # декоратор для обработчика команды start
async def start_command(message: types.Message):
    await message.reply(config.START_COMMAND_TEXT, reply_markup=kb.main)


@router.message(Command('help'))
@router.message(F.text == 'Помощь!')
async def help_command(message: types.Message):
    await message.reply(config.HELP_COMMAND_TEXT)


@router.message(F.text == 'Привет')
async def cmd_hello(message: types.Message):
    await message.answer('И вам привет!')


@router.message(Command('stop'))
@router.message(F.text == 'Стоп')
async def stop(message: types.Message):
    await message.reply("Пока!", reply_markup=ReplyKeyboardRemove())


@router.message(Command('recent'))
@router.message(F.text == 'Последнее событие')
async def recent_command(message: types.Message):
    await message.reply('Ваше последнее событие:')
    await message.reply(str(print_events(events)[-1]))


@router.message(Command('graph'))
@router.message(F.text == 'Моя статистика')
async def graph_command(message: types.Message):
    await message.reply('Выберите по чем составить статистику(последняя неделя):', reply_markup=kb.chose_type)


@router.message(Command('graph_place'))
@router.message(F.text == 'По локации')
async def graph_place_command(message: types.Message):
    await message.reply('Ваша статистика:')
    save_to_csv(events[-7:])
    df = pd.read_csv("google_calendar_events.csv")
    # print(df_fuel_engine_type)
    plt.figure(figsize=(8, 6))
    data = df['location'].value_counts()
    plt.pie(data.values,
            labels=data.keys(),
            autopct='%.2f%%',
            textprops={'fontsize': '10',
                       'fontweight': 'bold',
                       'color': 'white'
                       })
    plt.legend()
    plt.title('Распределение по месту:', fontsize=18, fontweight='bold')
    plt.savefig("graphs/img.pdf", format="pdf", bbox_inches="tight")
    async with ChatActionSender.upload_photo(bot=message.bot, chat_id=message.chat.id):
        media = MediaGroupBuilder(caption="")
        media.add_photo(FSInputFile('graphs/img.pdf'), 'Пирог!')
        await asyncio.sleep(1)
        await message.reply_media_group(media=media.build())


@router.message(Command('graph_color'))
@router.message(F.text == 'По цвету')
async def graph_place_command(message: types.Message):
    await message.reply('Ваша статистика:')
    save_to_csv(events[-7:])
    df = pd.read_csv("google_calendar_events.csv")
    # print(df_fuel_engine_type)
    plt.figure(figsize=(8, 6))
    data = df['color_name'].value_counts()
    plt.pie(data.values,
            labels=data.keys(),
            autopct='%.2f%%',
            textprops={'fontsize': '10',
                       'fontweight': 'bold',
                       'color': 'white'
                       })
    plt.legend()
    plt.title('Распределение по цвету:', fontsize=18, fontweight='bold')
    plt.savefig("graphs/img.pdf", format="pdf", bbox_inches="tight")
    async with ChatActionSender.upload_photo(bot=message.bot, chat_id=message.chat.id):
        media = MediaGroupBuilder(caption="")
        media.add_photo(FSInputFile('graphs/img.pdf'), 'Не пирог!')
        await asyncio.sleep(1)
        await message.reply_media_group(media=media.build())

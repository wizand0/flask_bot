import requests
from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command


router = Router()


@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer("Привет! Я помогу тебе узнать твой ID, просто отправь мне любое сообщение")



# При получении команды "Dict" выполняется перевод переданного слова@router.message(Command("dict"))
async def get_info(msg: Message):
    url = 'https://api.dictionaryapi.dev/api/v2/entries/en/{}'.format(word)
    response = requests.get(url)
# return a custom response if an invalid word is provided
    if response.status_code == 404:
        error_response = 'We are not able to provide any information about your word. Please confirm that the word is ' \
                         'spelled correctly or try the search again at a later time.'
        return error_response
    data = response.json()[0]
    await msg.answer(data)



async def start_handler(msg: Message):
    await msg.answer("Привет! Я помогу тебе узнать твой ID, просто отправь мне любое сообщение")






@router.message()
async def message_handler(msg: Message):
    await msg.answer(f"Твой ID: {msg.from_user.id}")
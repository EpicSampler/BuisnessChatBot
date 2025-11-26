from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import ollama
from decouple import config

help = open('C:/Users/mm1/Desktop/Buisness Chat Bot/BuisnessChatBot/BuisnessBot/TelegramBot/handlers/txts/help.txt', 'r')
model = config('MODEL')

start_router = Router()

@start_router.message(CommandStart())
async def start(message: Message):
    await message.answer('Здравствуйте, бот готов к работе. Можете задавать свой вопрос.')

@start_router.message(F.text == '/help')
async def help(message: Message):
    await message.answer(str(help.readlines()))
    

@start_router.message(F.text)
async def question(message: Message):
    try:
        response = ollama.generate(
            model = model,
            messages=[
                {'role': 'system', 'content': 'Ты - помощник в крупной IT-компании. К тебе могут обращаться как сотрудники компании, так и ее клиенты. Твоя задача - давать понятные всем инструкции по решению их проблем'},
                {'role': 'user', 'content': message.text}
            ]
        )
        print(response)
        await message.answer(response['message']['content'])
    except:
       await message.answer('Во время получения ответа произошла ошибка, повторите попытку позже.')
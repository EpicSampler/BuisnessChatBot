from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import ollama
from decouple import config
import textwrap
import os

BASE_DIR = os.getcwd()
gg = os.path.join(BASE_DIR, 'BuisnessBot', 'TelegramBot', 'handlers', 'txts', 'help.txt')
fil = open(gg, 'r', encoding='UTF-8')
helpf = ''
for i in fil.readlines():
    helpf += i
fil.close()

model = config('MODEL')

start_router = Router()

def get_resp(message):
    print('try to get response')
    response = ollama.chat(
        model = model,
        messages=[
            {'role': 'system', 'content': 'Ты - помощник в крупной IT-компании. К тебе могут обращаться как сотрудники компании, так и ее клиенты. Твоя задача - давать понятные всем инструкции по решению их проблем, используй сдержанный язык - без восклицаний, только официально-деловой стиль'},
            {'role': 'user', 'content': message}
        ],
        stream=False
    )

    answer = response['message']['content']
    return answer


@start_router.message(CommandStart())
async def start(message: Message):
    await message.answer('Здравствуйте, бот готов к работе. Можете задавать свой вопрос.')

@start_router.message(Command('help'))
async def send_help(message: Message):
    await message.answer(helpf)
    
@start_router.message(F.text)
async def question(message: Message):
    try:
        await message.answer('Ответ подготавливается...')

        answer = get_resp(message.text)
        
        answers = textwrap.wrap(answer, 4000)

        for i in answers:
            await message.answer(i)

    except Exception as error:
       print(f'error occured while sending message {error}')
       await message.answer('Во время получения ответа произошла ошибка, повторите попытку позже.')
from openai import OpenAI
import time

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message


import asyncio
import logging
import dotenv
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

dotenv.load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")


dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я бот для тз")
    
    
@dp.message()
async def handle_massege(message: types.Message):
    quest = message.text
    await message.answer('Идет анализ...')
    
    prompt_template = """# Роль
Ты — эксперт по анализу коммуникаций и customer service. Твоя задача — мгновенно анализировать тон телефонных разговоров и давать конкретные рекомендации.

# Задача
Проанализируй предоставленный диалог и определи его эмоциональную окраску. Затем предложи практические советы для улучшения подобных разговоров.

# Критерии анализа тона
• Позитивный - доброжелательный тон, улыбка в голосе, согласие, благодарность
• Нейтральный - деловой стиль, без эмоций, фактологический обмен
• Негативный - раздражение, гнев, сарказм, отказ, прерывание

# Правила ответа
- Отвечай только на русском
- Формат строго без лишних слов:
Тон разговора: [категория]

Советы:
1. [Конкретное действие]
2. [Конкретное действие]

- Не добавляй пояснений, приветствий или заключений
- Анализируй только фактический текст диалога
- Давай максимально практические рекомендации
- Время ответа должно быть минимальным

# Примеры
Диалог: "Спасибо за помощь! Вы мне очень помогли"
Ответ: 
Тон разговора: позитивный

Советы:
1. Поблагодарить клиента за обратную связь
2. Предложить дополнительную помощь если потребуется

Диалог: "Мне всё равно что вы предлагаете. Не звоните больше"
Ответ:
Тон разговора: негативный

Советы:
1. Немедленно извиниться за беспокойство
2. Внести номер в стоп-лист для исключения повторных звонков

# Анализируемый диалог:{quest}"""


    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=DEEPSEEK_API_KEY,
    )


    completion = client.chat.completions.create(
    extra_headers={
        "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
        "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
    },
    extra_body={},
    model="deepseek/deepseek-r1:free",
    messages=[
        {
        "role": "user",
        "content": prompt_template,
        }
    ]
    )

    answer = completion.choices[0].message.content
    await message.answer(answer)


async def main():
    bot = Bot(TOKEN)
    await dp.start_polling(bot)
    
    
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен!')

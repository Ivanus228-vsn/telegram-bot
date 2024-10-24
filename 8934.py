import asyncio
import aiohttp
import random
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardMarkup
from bs4 import BeautifulSoup
import ssl

bot = Bot(token='7610621865:AAEaO79SFrYP6gwGWXxSePHxFRgVEhP3jc8')
dp = Dispatcher()

horoscope_urls = {
    'овен': {
        'url': 'https://horo.mail.ru/prediction/aries/today/',
        'selector': '#horo-app-root > div.rb-p-branding--body > div.rb-p-branding--content.rb-p-branding--wrapper > div:nth-child(1) > div > div > div > section > main > div > div:nth-child(1) > div > div:nth-child(2) > section > section > main > div:nth-child(1) > div > p'
    },
    'телец': {
        'url': 'https://horo.mail.ru/prediction/taurus/today/',
        'selector': '#horo-app-root > div.rb-p-branding--body > div.rb-p-branding--content.rb-p-branding--wrapper > div:nth-child(1) > div > div > div > section > main > div > div:nth-child(1) > div > div:nth-child(2) > section > section > main > div:nth-child(2) > div > p'
    },
    'близнецы': {
        'url': 'https://horo.mail.ru/prediction/gemini/today/',
        'selector': '#horo-app-root > div.rb-p-branding--body > div.rb-p-branding--content.rb-p-branding--wrapper > div:nth-child(1) > div > div > div > section > main > div > div:nth-child(1) > div > div:nth-child(2) > section > section > main > div:nth-child(1) > div > p'
    },
    'рак': {
        'url': 'https://horo.mail.ru/prediction/cancer/today/',
        'selector': '#horo-app-root > div.rb-p-branding--body > div.rb-p-branding--content.rb-p-branding--wrapper > div:nth-child(1) > div > div > div > section > main > div > div:nth-child(1) > div > div:nth-child(2) > section > section > main > div:nth-child(1) > div > p'
    },
    'лев': {
        'url': 'https://horo.mail.ru/prediction/leo/today/',
        'selector': '#horo-app-root > div.rb-p-branding--body > div.rb-p-branding--content.rb-p-branding--wrapper > div:nth-child(1) > div > div > div > section > main > div > div:nth-child(1) > div > div:nth-child(2) > section > section > main > div:nth-child(2) > div > p'
    },
    'дева': {
        'url': 'https://horo.mail.ru/prediction/virgo/today/',
        'selector': '#horo-app-root > div.rb-p-branding--body > div.rb-p-branding--content.rb-p-branding--wrapper > div:nth-child(1) > div > div > div > section > main > div > div:nth-child(1) > div > div:nth-child(2) > section > section > main > div:nth-child(1) > div > p'
    },
    'весы': {
        'url': 'https://horo.mail.ru/prediction/libra/today/',
        'selector': '#horo-app-root > div.rb-p-branding--body > div.rb-p-branding--content.rb-p-branding--wrapper > div:nth-child(1) > div > div > div > section > main > div > div:nth-child(1) > div > div:nth-child(2) > section > section > main > div:nth-child(1) > div > p'
    },
    'скорпион': {
        'url': 'https://horo.mail.ru/prediction/scorpio/today/',
        'selector': '#horo-app-root > div.rb-p-branding--body > div.rb-p-branding--content.rb-p-branding--wrapper > div:nth-child(1) > div > div > div > section > main > div > div:nth-child(1) > div > div:nth-child(2) > section > section > main > div:nth-child(1) > div > p'
    },
    'стрелец': {
        'url': 'https://horo.mail.ru/prediction/sagittarius/today/',
        'selector': '#horo-app-root > div.rb-p-branding--body > div.rb-p-branding--content.rb-p-branding--wrapper > div:nth-child(1) > div > div > div > section > main > div > div:nth-child(1) > div > div:nth-child(2) > section > section > main > div:nth-child(1) > div > p'
    },
    'козерог': {
        'url': 'https://horo.mail.ru/prediction/capricorn/today/',
        'selector': '#horo-app-root > div.rb-p-branding--body > div.rb-p-branding--content.rb-p-branding--wrapper > div:nth-child(1) > div > div > div > section > main > div > div:nth-child(1) > div > div:nth-child(2) > section > section > main > div:nth-child(1) > div > p'
    },
    'водолей': {
        'url': 'https://horo.mail.ru/prediction/aquarius/today/',
        'selector': '#horo-app-root > div.rb-p-branding--body > div.rb-p-branding--content.rb-p-branding--wrapper > div:nth-child(1) > div > div > div > section > main > div > div:nth-child(1) > div > div:nth-child(2) > section > section > main > div:nth-child(1) > div > p'
    },
    'рыбы': {
        'url': 'https://horo.mail.ru/prediction/pisces/today/',
        'selector': '#horo-app-root > div.rb-p-branding--body > div.rb-p-branding--content.rb-p-branding--wrapper > div:nth-child(1) > div > div > div > section > main > div > div:nth-child(1) > div > div:nth-child(2) > section > section > main > div:nth-child(1) > div > p'
    }
}

predictions = [
    'Сегодня отличный день для новых начинаний!',
    'Будьте внимательны к своим финансам.',
    'Вас ждет приятный сюрприз.',
    'Не упустите возможность поговорить с близким человеком.',
    'Сегодня вы сможете решить давнюю проблему.',
    'Не хочешь сладкого? Пей сухое!',
    'Вы проснетесь от поцелуя и аромата кофе.',
    'Обратите внимание на брюнетку напротив.',
    'Это послание из другой галактики самому доброму человеку. Миссия завершена успешно!',
    'Ты справишься!',
    'Твое счастье рядом!',
    'Через час ты снова проголодаешься. "Печеньем Удачи" не наешься.  :-)'
    'Смейся всегда беспечно, чтобы счастье длилось вечно.'
    'Родители замыслили что-то доброе.'
    'Если Вы проявите инициативу, успех не заставит себя ждать.'
    'Готовьтесь к романтическим приключениям.'
    'В этом месяце ночная жизнь для вас.'
    'Вам пора отдохнуть.'
    'Вам предлагается мечта всей жизни. Скажите да!'
    'Вас ждет приятный сюрприз.'
    'Ваши надежды и планы сбудутся сверх всяких ожиданий.'
    'Время – ваш союзник, лучше отложить принятие важного решения хотя бы на день.'
    'Время и терпение,  вас ждут много сюрпризов!'
    'Время осушит все слезы и исцелит все раны.'
]


@dp.message(Command('start'))
async def send_welcome(message: Message):
    kb = [
        [
            types.KeyboardButton(text='что меня ждет сегодня?'),
            types.KeyboardButton(text='хочу предсказание!'),
            types.KeyboardButton(text='я не верю в гороскопы'),
            types.KeyboardButton(text='помоги принять решение')  # Новая кнопка
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )
    await message.answer("привет! я бот, который поможет тебе заглянуть в будущее с помощью гороскопа",
                         reply_markup=keyboard)

@dp.message(lambda message: message.text.lower() == 'что меня ждет сегодня?')
async def handle_today(message: Message):
    await message.answer(f"{message.from_user.first_name}, кто ты по знаку зодиака?",
                         reply_markup=ReplyKeyboardRemove())

@dp.message(lambda message: message.text.lower() in horoscope_urls.keys())
async def get_horoscope(message: Message):
    zodiac_sign = message.text.lower()
    horoscope = await fetch_horoscope(zodiac_sign)
    await message.answer(horoscope)

async def fetch_horoscope(zodiac_sign: str) -> str:
    url = horoscope_urls[zodiac_sign]['url']
    selector = horoscope_urls[zodiac_sign]['selector']

    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, ssl=ssl_context) as response:
                if response.status == 200:
                    html = await response.text()
                    return parse_horoscope(html, selector)
                else:
                    return "Не удалось получить информацию о гороскопе."
        except Exception as e:
            return f"Произошла ошибка: {str(e)}"

def parse_horoscope(html: str, selector: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    horoscope_element = soup.select_one(selector)

    if horoscope_element:
        return horoscope_element.get_text(strip=True)
    else:
        return "Не удалось найти гороскоп."

@dp.message(lambda message: message.text.lower() == 'хочу предсказание!')
async def handle_prediction(message: Message):
    prediction = random.choice(predictions)
    await message.answer(prediction)

@dp.message(lambda message: message.text.lower() == 'я не верю в гороскопы')
async def handle_no_horoscope(message: Message):
    await message.answer(f"{message.from_user.first_name}, так поверь", reply_markup=ReplyKeyboardRemove())

@dp.message(lambda message: message.text.lower() == 'помоги принять решение')
async def help_decision(message: Message):
    decision = random.choice(['да', 'нет'])
    await message.answer(decision)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
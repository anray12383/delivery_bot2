from typing import List

import gino
from aiogram import types, Bot, Dispatcher
import logging
from aiogram.utils import executor
import emoji
from config import BOT_TOKEN, POSTGRES_URI
from utils.db_api.database import db, connect_db
from utils.db_api.db_commands import get_rests_names, get_courses_names
from utils.db_api.models import Rest
import asyncio

async def main():
    name = await get_rests_names()
    for i in name:
        print(f'{i.rest_name}')


async def trying_k():
    rest_name = 'Old Bukhara'
    course_type = 'salade'
    result = await get_courses_names(rest_name, course_type)
    for course in result:
        print(f"{course.name} - {course.price}")
    courses = await get_courses_names(rest_name, course_type)
    for course in courses:
        # Сформируем текст, который будет на кнопке
        button_text = f'Купить {course.name} за {course.price}'
        print(button_text)




loop = asyncio.get_event_loop()
loop.run_until_complete(connect_db())
loop.run_until_complete(main())
loop.run_until_complete(trying_k())


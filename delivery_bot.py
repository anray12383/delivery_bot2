import asyncio
from typing import Union

from aiogram import executor
from aiogram import types
from aiogram.types import CallbackQuery, Message

from config import dp
from keyboards import menu_cd, rests_names_keyboard, courses_names_keyboard, start_menu_keyboard, courses_types_keyboard
from utils.db_api.database import connect_db


# Хендлер на команду /start
@dp.message_handler(commands=["start"])
async def show_menu(message: types.Message):
    markup = await start_menu_keyboard()
    # Выполним функцию, которая отправит пользователю кнопки с доступными категориями
    await message.answer('Добро пожаловать!\nЧего вы желаете?', reply_markup=markup)


@dp.message_handler(content_types=['text'])
async def main_menu_handler(message: types.Message):
    if 'Рестораны' in message.text:
        await list_rests_names(message)


# Та самая функция, которая отдает категории. Она может принимать как CallbackQuery, так и Message
# Помимо этого, мы в нее можем отправить и другие параметры - category, subcategory, item_id,
# Поэтому ловим все остальное в **kwargs
async def list_rests_names(message: Union[CallbackQuery, Message], **kwargs):
    # Клавиатуру формируем с помощью следующей функции (где делается запрос в базу данных)
    markup = await rests_names_keyboard()

    # Проверяем, что за тип апдейта. Если Message - отправляем новое сообщение
    if isinstance(message, Message):
        await message.answer("Выберите ресторан:", reply_markup=markup)

    # Если CallbackQuery - изменяем это сообщение
    elif isinstance(message, CallbackQuery):
        call = message
        await call.message.edit_reply_markup(markup)


# Функция, которая отдает кнопки с типами блюд
async def list_courses_types(callback: CallbackQuery, rest_name, **kwargs):
    markup = await courses_types_keyboard(rest_name)

    # Изменяем сообщение, и отправляем новые кнопки с подкатегориями
    await callback.message.edit_text(text="Смотри, что у нас есть:", reply_markup=markup)


# Функция, которая отдает кнопки с названиями блюд, по выбранному пользователем ресторану и типу блюд
async def list_courses_names(callback: CallbackQuery, rest_name, course_type, **kwargs):
    markup = await courses_names_keyboard(rest_name, course_type)

    # Изменяем сообщение, и отправляем новые кнопки с подкатегориями
    await callback.message.edit_text(text="Смотри, что у нас есть:", reply_markup=markup)


# # Функция, которая отдает кнопки с названием и ценой блюда, по выбранным ресторану и блюду
# async def list_items(callback: CallbackQuery, rest_name, course_name, **kwargs):
#     markup = await items_keyboard(rest_name, course_name)
#
#     # Изменяем сообщение, и отправляем новые кнопки с подкатегориями
#     await callback.message.edit_text(text="Смотри, что у нас есть", reply_markup=markup)
#
#
# # Функция, которая отдает уже кнопку Купить товар по выбранному товару
# async def show_item(callback: CallbackQuery, category, subcategory, item_id):
#     markup = item_keyboard(category, subcategory, item_id)
#
#     # Берем запись о нашем товаре из базы данных
#     item = await get_item(item_id)
#     text = f"Купи {item.name}"
#     await callback.message.edit_text(text=text, reply_markup=markup)


# Функция, которая обрабатывает ВСЕ нажатия на кнопки в этой менюшке
@dp.callback_query_handler(menu_cd.filter())
async def navigate(call: CallbackQuery, callback_data: dict):
    """

    :param call: Тип объекта CallbackQuery, который прилетает в хендлер
    :param callback_data: Словарь с данными, которые хранятся в нажатой кнопке
    """

    # Получаем текущий уровень меню, который запросил пользователь
    current_level = callback_data.get("level")

    # Получаем категорию, которую выбрал пользователь (Передается всегда)
    rest_name = callback_data.get("rest_name")

    course_type = callback_data.get("course_type")

    # Получаем подкатегорию, которую выбрал пользователь (Передается НЕ ВСЕГДА - может быть 0)
    course_name = callback_data.get("course_name")


    # Прописываем "уровни" в которых будут отправляться новые кнопки пользователю
    levels = {
        "0": list_rests_names,  # Отдаем категории
        "1": list_courses_types,  # Отдаем подкатегории
        "2": list_courses_names,  # Отдаем товары
        # "3": show_item  # Предлагаем купить товар
    }

    # Забираем нужную функцию для выбранного уровня
    current_level_function = levels[current_level]

    # Выполняем нужную функцию и передаем туда параметры, полученные из кнопки
    await current_level_function(
        call,
        rest_name=rest_name,
        course_type=course_type,
        course_name=course_name
    )

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(connect_db())
    executor.start_polling(dp, skip_updates=True)

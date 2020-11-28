import emoji
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.callback_data import CallbackData

from utils.db_api.db_commands import get_rests_names, get_courses_names

# Создаем CallbackData-объекты, которые будут нужны для работы с менюшкой
menu_cd = CallbackData('show_menu', 'level', 'rest_name', 'course_type', 'course_name')
buy_course = CallbackData('buy', 'course_code')


# С помощью этой функции будем формировать коллбек дату для каждого элемента меню, в зависимости от
# переданных параметров. Если Подкатегория, или айди товара не выбраны - они по умолчанию равны нулю
def make_callback_data(level, rest_name='0', course_type='0', course_name='0'):
    return menu_cd.new(level=level, rest_name=rest_name, course_type=course_type, course_name=course_name)


async def start_menu_keyboard():
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    menu_button = types.KeyboardButton(emoji.emojize(':man_cook:') + ' Рестораны')
    cart_button = types.KeyboardButton(' Корзина')
    orders_button = types.KeyboardButton(' Заказы')
    promos_button = types.KeyboardButton(' Новости')
    settings_button = types.KeyboardButton(' Настройки')
    help_button = types.KeyboardButton(' Помощь')
    markup.add(menu_button, cart_button, orders_button, promos_button, settings_button, help_button)
    return markup


async def back_to_start_keyboard():
    back_key = ReplyKeyboardMarkup(resize_keyboard=True)
    back_to_start_button = KeyboardButton(' В начало')
    back_key.add(back_to_start_button)
    return back_key


# Создаем функцию, которая отдает клавиатуру с доступными категориями
async def rests_names_keyboard():
    # Указываем, что текущий уровень меню - 0
    CURRENT_LEVEL = 0

    # Создаем Клавиатуру
    markup = InlineKeyboardMarkup()

    # Забираем список ресторанов из базы данных и проходим по нему
    rests_names = await get_rests_names()
    for rest_name in rests_names:
        # Сформируем текст, который будет на кнопке
        button_text = f"{rest_name.rest_name}"
        # Сформируем колбек дату, которая будет на кнопке. Следующий уровень - текущий + 1, и перечисляем рестораны
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1, rest_name=rest_name.rest_name)

        # Вставляем кнопку в клавиатуру
        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )

    # Возвращаем созданную клавиатуру в хендлер
    return markup


# Создаем функцию, которая отдает клавиатуру с типами блюд, исходя из выбранного ресторана
async def courses_types_keyboard(rest_name):
    # Текущий уровень - 1
    CURRENT_LEVEL = 1
    markup = InlineKeyboardMarkup(row_width=2)
    appetizer_button = InlineKeyboardButton(text='Закуски', callback_data=make_callback_data(level=CURRENT_LEVEL + 1, rest_name=rest_name, course_type='appetizer'))
    salade_button = InlineKeyboardButton(text='Салаты', callback_data=make_callback_data(level=CURRENT_LEVEL + 1, rest_name=rest_name, course_type='salade'))
    first_course_button = InlineKeyboardButton(text='Первые блюда', callback_data=make_callback_data(level=CURRENT_LEVEL + 1, rest_name=rest_name, course_type='first_course'))
    main_course_button = InlineKeyboardButton(text='Основные блюда', callback_data=make_callback_data(level=CURRENT_LEVEL + 1, rest_name=rest_name, course_type='main_course'))
    desserts_button = InlineKeyboardButton(text='Десерты', callback_data=make_callback_data(level=CURRENT_LEVEL + 1, rest_name=rest_name, course_type='desserts'))
    drinks_button = InlineKeyboardButton(text='Напитки', callback_data=make_callback_data(level=CURRENT_LEVEL + 1, rest_name=rest_name, course_type='drinks'))
    markup.add(appetizer_button, salade_button, first_course_button, main_course_button, desserts_button, drinks_button)

    # Создаем Кнопку "Назад", в которой прописываем колбек дату такую, которая возвращает
    # пользователя на уровень назад - на уровень 0.
    markup.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=make_callback_data(level=CURRENT_LEVEL - 1))
    )
    return markup


# Создаем функцию, которая отдает клавиатуру с ценами блюд, кнопками купить и назад
# исходя из выбранного ресторана и типа блюд
async def courses_names_keyboard(rest_name, course_type):
    # Текущий уровень - 2
    CURRENT_LEVEL = 2
    markup = InlineKeyboardMarkup()

    # Забираем список товаров с РАЗНЫМИ подкатегориями из базы данных с учетом выбранной категории и проходим по ним
    courses = await get_courses_names(rest_name, course_type)
    for course in courses:

        # Сформируем текст, который будет на кнопке
        button_text = f'Купить {course.name} за {course.price}'
        # Сформируем колбек дату, которая будет на кнопке
        callback_data = buy_course.new(course_code=course.course_code)
        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )

    # Создаем Кнопку "Назад", в которой прописываем колбек дату такую, которая возвращает
    # пользователя на уровень назад - на уровень 0.
    markup.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=make_callback_data(level=CURRENT_LEVEL - 1))
    )
    return markup

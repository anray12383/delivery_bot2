import logging
from aiogram import executor
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import dp


class UserState(StatesGroup):
    State1 = State()
    State2 = State()
    State3 = State()


@dp.message_handler(commands='start', state=None)
async def start_handler(message: types.Message):
    key_markup = types.InlineKeyboardMarkup()
    hi_butt = types.InlineKeyboardButton(text='Hi!', callback_data='Hi')
    key_markup.add(hi_butt)
    await message.answer("Hi!", reply_markup=key_markup)
    await UserState.first()


@dp.callback_query_handler(state=UserState.State1)
async def ans_1(callback: CallbackQuery, state: FSMContext):
    markup = InlineKeyboardMarkup()
    yes_butt = InlineKeyboardButton('Да', callback_data='да')
    no_butt = InlineKeyboardButton('Нет', callback_data='нет')
    markup.add(yes_butt, no_butt)
    await callback.message.answer(text="Запрос 1", reply_markup=markup)
    await UserState.next()


@dp.callback_query_handler(state=UserState.State2)
async def ans_2(callback: CallbackQuery, state: FSMContext):
    markup = InlineKeyboardMarkup()
    yes_butt = InlineKeyboardButton('Да', callback_data='да')
    no_butt = InlineKeyboardButton('Нет', callback_data='нет')
    markup.add(yes_butt, no_butt)
    markup.row(InlineKeyboardButton(text='Назад', callback_data='back'))
    await callback.message.answer(text="Запрос 2", reply_markup=markup)
    await UserState.next()


@dp.callback_query_handler(state='*')
async def back(callback: CallbackQuery):
    if callback.data == 'back':
        await UserState.previous()
    else:
        return


@dp.callback_query_handler(state=UserState.State3)
async def ans_3(callback: CallbackQuery, state: FSMContext):
    markup = InlineKeyboardMarkup()
    yes_butt = InlineKeyboardButton('Да', callback_data='да')
    no_butt = InlineKeyboardButton('Нет', callback_data='нет')
    markup.add(yes_butt, no_butt)
    markup.row(InlineKeyboardButton(text='Назад', callback_data='back'))
    await callback.message.answer(text="Запрос 3", reply_markup=markup)
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)


 if bottom and falling and self.y == 0 \
         and co.y2 < self.game.canvas_height \
         and collided_bottom(1, co, sprite_co):
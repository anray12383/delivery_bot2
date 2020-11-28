from aiogram.dispatcher.filters.state import StatesGroup, State


class ChoiceState(StatesGroup):
    rest_choice = State()
    course_type_choice = State()
    course_choice = State()

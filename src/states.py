from aiogram.dispatcher.filters.state import State, StatesGroup


class UserState(StatesGroup):
    wait_type_of_order = State()
    wait_number_hoockah = State()
    wait_info_about_order = State()
    wait_tobacco_strength = State()
    wait_tobacco_flavor = State()
    wait_cup = State()
    wait_phone_number = State()
    wait_time = State()
    wait_correct = State()


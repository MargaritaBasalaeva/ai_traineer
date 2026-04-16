from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_keyboard(count: int):
    keyb = InlineKeyboardBuilder()

    keyb.button(text="➖", callback_data=f"operation_minus_{count}")
    keyb.button(text="+", callback_data=f"operation_plus_{count}")
    keyb.button(text="🔄 начать сначала", callback_data="reset")
    keyb.button(text="Выбрать другую тренировку", callback_data="main_menu")


    keyb.adjust(1)
    return keyb.as_markup()

menu = InlineKeyboardMarkup(
    inline_keyboard = [
        [InlineKeyboardButton(text = 'Выбрать тренировку', callback_data="main_menu")
         ]])

days = InlineKeyboardMarkup(
    inline_keyboard = [
        [InlineKeyboardButton(text = 'День ног', callback_data = 'day_legs')],
        [InlineKeyboardButton(text = 'День рук', callback_data = 'day_arms')],
        [InlineKeyboardButton(text = 'Кардио', callback_data = 'day_cardio')]
    ]
)

def get_answer_keyboard(day_name):
    answ = InlineKeyboardBuilder()

    answ.button(text = 'Да, погнали!', callback_data = f'answ_yes_{day_name}')
    answ.button(text = 'Нет, сделай ещё раз', callback_data = f'answ_no_{day_name}')
    answ.button(text = 'Выбрать другую тренировку', callback_data="main_menu")

    answ.adjust(2)
    return answ.as_markup()
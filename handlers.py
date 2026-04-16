from aiogram.filters.command import Command
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
import keyboards as kb
import random
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import ReplyKeyboardRemove

user = Router()

d = {'legs':'день ног', 'arms': 'день рук', 'cardio': 'день кардио'}

@user.message(F.text == 'Составить тренировку')
async def cmd_hello(message: Message):
    await message.answer(
        'Выбери вариант тренировки',
        reply_markup=ReplyKeyboardRemove()  # 👈 убрали старую
    )

def exerc(day_name, nums=5):
    exercises = {
        'legs': [
            'Жим ногами', 'Сгибание голени', 'Разгибание голени',
            'Разгибание бедра', 'Маятниковый присед',
            'Силовой присед', 'Румынская тяга', 'Смит-присед'
        ],
        'arms': [
            'Горизонтальная тяга', 'Вертикальная тяга', 'Экстензия',
            'Косичка', 'Жим от плеч', 'Пресс',
            'Отжимания', 'Подтягивания', 'Планка'
        ],
        'cardio': [
            'Лестница', 'Эллипс', 'Беговая дорожка'
        ]
    }

    random_cardio = []

    if day_name == 'cardio':
        nums = 1
    else:
        p = random.randint(0, 1)
        if p != 0:
            random_cardio = [f'🎁 Бонус: {random.sample(exercises.get('cardio', []), 1)[0]} 15-30 минут']
    return random.sample(exercises.get(day_name, []), nums) + random_cardio


@user.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Привет! Это твой персональный ИИ тренер, с которым можно составлять расписание тренировок.",
                         reply_markup = kb.menu)

@user.callback_query(F.data == 'main_menu')
async def cmd_hello(callback: CallbackQuery):
    await callback.message.answer('Выбери вариант тренировки',
                         reply_markup = kb.days)


@user.callback_query(F.data.startswith('day_'))
async def check_day(callback: CallbackQuery):
    day_name = callback.data.split('_')[1]
    await callback.answer(f'Вы выбрали {d[day_name]}', show_alert = True)
    await callback.message.answer(f'Вы выбрали {d[day_name]}')
    random_ex = exerc(day_name)
    await callback.message.answer('💪 Список упражнений на сегодня для тебя:\n\n' + '\n\n'.join(random_ex) + '\n\n'+ '🌼 Устраивает ли тебя данный выбор?',
                                  reply_markup = kb.get_answer_keyboard(day_name))



@user.callback_query(F.data.startswith('answ_'))
async def check_answ(callback: CallbackQuery):
    _, answ_name, day_name = callback.data.split('_')


    if answ_name == 'yes':
        nums = 5
        if day_name != 'cardio':
            await callback.message.answer(
                f'Отлично!\n\nОсталось подходов: {nums}',
                reply_markup=kb.get_keyboard(nums)
            )
        else:
            await callback.message.answer(
                'Отлично!\n\n 🏃‍♀️ Удачной ходьбы',
                reply_markup = kb.menu
            )

    elif answ_name == 'no':
        random_ex = exerc(day_name)
        try:
            await callback.message.edit_text(
                '💪 Список упражнений на сегодня для тебя:\n\n' + '\n\n'.join(random_ex) + '\n\n'+ '🌼 Устраивает ли тебя данный выбор?',
                reply_markup=kb.get_answer_keyboard(day_name)
            )
        except TelegramBadRequest as e:
            if "message is not modified" in str(e):
                await callback.message.edit_text('💪 Список упражнений на сегодня для тебя:\n\n' +
                                                 '\n\n'.join(random_ex) + '\n\n' +'Выпал тот же вариант😅\n\n Попробуй ещё раз ☺️',
                                                 reply_markup=kb.get_answer_keyboard(day_name))

    await callback.answer()



@user.callback_query(F.data.startswith("operation"))
async def decrement_handler(callback: CallbackQuery):
    count = int(callback.data.split("_")[2])
    oper = callback.data.split("_")[1]
    if count > 0:
        if oper == 'minus':
            count -= 1
        elif oper == 'plus':
            count += 1
    try:
        if count == 0:
            text = "Подходы закончились 🎉\nНажми «начать сначала»"
        else:
            text = f"Осталось подходов: {count}"

        await callback.message.edit_text(
            text,
            reply_markup=kb.get_keyboard(count)
        )
    except TelegramBadRequest as e:
            if "message is not modified" in str(e):
                return

    await callback.answer()

# --- сброс ---
@user.callback_query(F.data == "reset")
async def reset_handler(callback: CallbackQuery):
    start_count = 5

    await callback.message.edit_text(
        f"Подходы: {start_count}",
        reply_markup=kb.get_keyboard(start_count)
    )

    await callback.answer()
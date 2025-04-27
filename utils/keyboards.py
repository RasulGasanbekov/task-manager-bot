from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def category_keyboard():
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Учеба")],
            [KeyboardButton(text="Личное")],
            [KeyboardButton(text="Другое")]
        ],
        resize_keyboard=True
    )
    return kb

def priority_keyboard():
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Высокий")],
            [KeyboardButton(text="Средний")],
            [KeyboardButton(text="Низкий")]
        ],
        resize_keyboard=True
    )
    return kb
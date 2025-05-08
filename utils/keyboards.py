from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton,InlineKeyboardMarkup

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

def get_reminder_keyboard(task_id: int):
    buttons = [
        [
            InlineKeyboardButton(text="📅 За 1 день", callback_data=f"remind_{task_id}_1"),
            InlineKeyboardButton(text="📅 За 3 дня", callback_data=f"remind_{task_id}_3")
        ],
        [
            InlineKeyboardButton(text="📅 За 7 дней", callback_data=f"remind_{task_id}_7")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
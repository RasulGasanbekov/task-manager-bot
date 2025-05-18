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


def get_category_keyboard():
    kb = [
        [InlineKeyboardButton(text="📚 Учеба", callback_data="category_учеба")],
        [InlineKeyboardButton(text="🏠 Личное", callback_data="category_личное")],
        [InlineKeyboardButton(text="📦 Другое", callback_data="category_другое")],
        [InlineKeyboardButton(text="🌐 Все", callback_data="category_все")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


def get_priority_keyboard():
    kb = [
        [InlineKeyboardButton(text="❗ Высокий", callback_data="priority_высокий")],
        [InlineKeyboardButton(text="🔺 Средний", callback_data="priority_средний")],
        [InlineKeyboardButton(text="🔻 Низкий", callback_data="priority_низкий")],
        [InlineKeyboardButton(text="❓ Не важно", callback_data="priority_any")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


def get_period_keyboard():
    kb = [
        [InlineKeyboardButton(text="📆 Сегодня", callback_data="period_today")],
        [InlineKeyboardButton(text="🗓️ Эта неделя", callback_data="period_week")],
        [InlineKeyboardButton(text="📅 Этот месяц", callback_data="period_month")],
        [InlineKeyboardButton(text="📅 Выбрать в календаре", callback_data="period_custom")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)
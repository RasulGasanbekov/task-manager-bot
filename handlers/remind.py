from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from database import crud
from utils.keyboards import get_reminder_keyboard

router = Router()

@router.message(F.text.startswith("/remind"))
async def remind_setup(message: Message):
    text = message.text.strip()
    parts = text.split()

    if len(parts) < 2:
        await message.answer("❌ Укажите ID задачи. Пример: <code>/remind 1</code>", parse_mode="HTML")
        return

    try:
        task_id = int(parts[1])
    except ValueError:
        await message.answer("❌ ID должен быть числом.")
        return

    task = crud.get_task_by_id(user_id=message.from_user.id, task_id=task_id)
    if not task:
        await message.answer(f"❌ Задача с ID {task_id} не найдена.")
        return

    await message.answer(
        "🔔 Выберите, за сколько дней до дедлайна получать напоминание:",
        reply_markup=get_reminder_keyboard(task_id)
    )

@router.callback_query(F.data.startswith("remind_"))
async def handle_reminder_choice(callback: CallbackQuery):
    data = callback.data.split("_")  
    if len(data) < 3:
        await callback.answer("❌ Ошибка: неверные данные.")
        return

    task_id = int(data[1])
    days = int(data[2])

    crud.update_task_reminder(task_id=task_id, reminder_days=days)

    await callback.message.edit_text(f"✅ Напоминание установлено за {days} {'день' if days == 1 else 'дня'} до дедлайна.")
    await callback.answer("🔔 Напоминание настроено!")
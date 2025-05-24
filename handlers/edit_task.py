from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from utils import keyboards
from database import crud
from datetime import datetime
from aiogram.types import ReplyKeyboardRemove
from database import crud, SessionLocal


class EditTask(StatesGroup):
    title = State()
    deadline = State()
    category = State()
    priority = State()


router = Router()


async def start_editing_flow(message: Message, task_id: int, state: FSMContext):
    """Запускает процесс редактирования"""

    task = crud.get_task_by_id(task_id)
    if not task:
        await message.answer("❌ Задача не найдена")
        return False

    await state.set_state(EditTask.title)
    await state.update_data(task_id=task_id, current_title=task.title)
    await message.answer(
        f"✏️ Редактирование задачи: <b>{task.title}</b>\n\n" "Введите новое название: ",
        parse_mode="HTML",
    )
    return True


@router.message(EditTask.title)
async def process_new_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(EditTask.deadline)
    await message.answer("📅 Введите новый дедлайн (ДД.ММ.ГГГГ ЧЧ:ММ)")


@router.message(EditTask.deadline)
async def edit_task_category(message: Message, state: FSMContext):
    try:
        deadline = datetime.strptime(message.text, "%d.%m.%Y %H:%M")
        await state.update_data(deadline=deadline)
        await state.set_state(EditTask.category)
        await message.answer(
            "📁 Выберите новую категорию:", reply_markup=keyboards.category_keyboard()
        )
    except ValueError:
        await message.answer("⚠️ Неверный формат даты. Используйте: ДД.ММ.ГГГГ ЧЧ:ММ")


@router.message(EditTask.category)
async def edit_task_priority(message: Message, state: FSMContext):
    await state.update_data(category=message.text)
    await state.set_state(EditTask.priority)
    await message.answer(
        "🔺 Выберите новый приоритет:", reply_markup=keyboards.priority_keyboard()
    )


@router.message(EditTask.priority)
async def save_edited_task(message: Message, state: FSMContext):
    user_data = await state.get_data()
    task_id = user_data["task_id"]

    crud.update_task(
        task_id=task_id,
        title=user_data["title"],
        deadline=user_data["deadline"],
        category=user_data["category"],
        priority=message.text,
        status="pending",
    )

    await state.clear()
    await message.answer(
        "✅ Задача успешно обновлена!", reply_markup=ReplyKeyboardRemove()
    )

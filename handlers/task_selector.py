from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from database import crud, SessionLocal
from handlers.edit_task import start_editing_flow
from handlers.remind import remind_setup
from utils.keyboards import (
    get_category_keyboard,
    get_priority_keyboard,
    get_tasks_keyboard,
)

router = Router()


class TaskSelector(StatesGroup):
    category = State()
    priority = State()
    select_task = State()


async def start_task_selection(message: Message, state: FSMContext, action: str):
    """Общая функция для начала выбора задачи"""
    await state.update_data(action=action)
    await state.set_state(TaskSelector.category)
    await message.answer(
        "📂 Выберите категорию задачи:", reply_markup=get_category_keyboard()
    )


@router.callback_query(TaskSelector.category, F.data.startswith("category_"))
async def process_category(callback: CallbackQuery, state: FSMContext):
    category = callback.data.split("_")[1].lower()
    await state.update_data(category=category)
    await state.set_state(TaskSelector.priority)
    await callback.message.edit_text(
        "🔺 Выберите приоритет:", reply_markup=get_priority_keyboard()
    )


@router.callback_query(TaskSelector.priority, F.data.startswith("priority_"))
async def process_priority(callback: CallbackQuery, state: FSMContext):
    priority = callback.data.split("_")[1].lower()
    data = await state.get_data()
    category = data["category"]
    action = data["action"]

    tasks = crud.get_tasks_by_filters(
        user_id=callback.from_user.id,
        category=category,
        priority=priority,
        status="pending" if action == "done" else None,
    )

    if not tasks:
        await callback.message.edit_text("❌ Нет задач по выбранным критериям.")
        await state.clear()
        return

    await state.set_state(TaskSelector.select_task)
    await callback.message.edit_text(
        f"📋 Выберите задачу для {data['action']}:",  # Показываем действие (delete/done/edit)
        reply_markup=get_tasks_keyboard(tasks, action=data["action"]),
    )


@router.callback_query(F.data.startswith("task_action:"))
async def process_task_selection(callback: CallbackQuery, state: FSMContext):
    try:
        # Разбираем callback_data в формате "task_action:delete:123"
        _, action, task_id_str = callback.data.split(":")
        task_id = int(task_id_str)
        task = crud.get_task_by_id(task_id)
        if not task:
            await callback.answer("❌ Задача не найдена")
            return

        # Выполняем действие в зависимости от типа
        if action == "delete":
            await delete_task_by_id(callback.message, task_id)
        elif action == "done":
            await mark_task_done_by_id(callback.message, task_id)
        elif action == "edit":
            await start_edit_task(callback.message, task_id, state)
        elif action == "remind":
            await remind_setup(callback.message, task_id)
        else:
            await callback.answer("⚠️ Неизвестное действие")

    except ValueError:
        await callback.answer("❌ Ошибка обработки запроса")
    except Exception as e:
        await callback.answer(f"⚠️ Ошибка: {str(e)}")
    finally:
        await callback.answer()


async def delete_task_by_id(message: Message, task_id: int):
    """Логика удаления задачи"""
    task = crud.get_task_by_id(task_id)
    if task:
        crud.delete_task(task_id)
        await message.answer(f"🗑️ Задача '{task.title}' удалена!")
    else:
        await message.answer("❌ Задача не найдена.")


async def mark_task_done_by_id(message: Message, task_id: int):
    """Логика отметки выполнения"""
    task = crud.get_task_by_id(task_id)
    if task:
        crud.update_task_status(task_id, "completed")
        await message.answer(f"✅ Задача '{task.title}' выполнена!")
    else:
        await message.answer("❌ Задача не найдена.")


async def start_edit_task(message: Message, task_id: int, state: FSMContext):
    """Запускает редактирование через edit_task.py"""
    success = await start_editing_flow(message, task_id, state)
    if not success:
        await message.answer("❌ Не удалось начать редактирование")


@router.callback_query(F.data == "cancel_action")
async def cancel_action(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("❌ Действие отменено")
    await callback.answer()

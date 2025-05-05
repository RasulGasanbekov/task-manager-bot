from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from utils import keyboards
from database import crud
from datetime import datetime
from aiogram.types import ReplyKeyboardRemove


router = Router()

class AddTask(StatesGroup):
    title = State()
    deadline = State()
    category = State()
    priority = State()

@router.message(F.text == "/start")
async def start_command(message: Message):
    await message.answer(f"Привет, {message.from_user.first_name}! Я помогу тебе управлять задачами 🎯")

@router.message(F.text == "/help")
async def help_command(message: Message):
    await message.answer(
    "ℹ️ Доступные команды:\n\n"
    "- /start — запускает бота и приветствует вас.\n"
    "- /add — создаёт новую задачу. Бот попросит выбрать категорию, приоритет и ввести текст задачи.\n"
    "- /list — показывает все текущие задачи с их категориями и приоритетами.\n"
    "- /delete — позволяет удалить задачу по номеру из списка.\n"
    "- /help — выводит список всех доступных команд и их описание."
)

@router.message(F.text == "/list")
async def list_tasks(message: Message):
    tasks = crud.get_tasks_by_user(user_id=message.from_user.id)
    
    if not tasks:
        await message.answer("📭 У вас пока нет задач.", parse_mode="HTML")
        return

    response = "📌 Ваши задачи:\n\n"
    for idx, task in enumerate(tasks, 1):
        deadline_str = task.deadline.strftime("%d.%m %H:%M")
        response += (
            f"{idx}. <b>{task.title}</b>\n"
            f" <b>Дедлайн:</b> {deadline_str}\n"
            f" <b>Категория:</b> {task.category}\n"
            f" <b>Приоритет:</b> {task.priority}\n"
            "———————–———————–———————–———————–\n"
        )
        
    await message.answer(response, parse_mode="HTML")

@router.message(F.text == "/add")
async def add_task_start(message: Message, state: FSMContext):
    await state.set_state(AddTask.title)
    await message.answer("Введите название задачи:")

@router.message(AddTask.title)
async def add_task_deadline(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(AddTask.deadline)
    await message.answer("Укажите дедлайн (формат ДД.ММ.ГГГГ ЧЧ:ММ):")

@router.message(AddTask.deadline)
async def add_task_category(message: Message, state: FSMContext):
    try:
        deadline = datetime.strptime(message.text, "%d.%m.%Y %H:%M")
        await state.update_data(deadline=deadline)
        await state.set_state(AddTask.category)
        await message.answer("Выберите категорию:", reply_markup=keyboards.category_keyboard())
    except ValueError:
        await message.answer("Неверный формат даты. Пожалуйста, укажите в формате ДД.ММ.ГГГГ ЧЧ:ММ")

@router.message(AddTask.category)
async def add_task_priority(message: Message, state: FSMContext):
    await state.update_data(category=message.text)
    await state.set_state(AddTask.priority)
    await message.answer(
        "Выберите приоритет:",
        reply_markup=keyboards.priority_keyboard()
    )

@router.message(AddTask.priority)
async def save_task(message: Message, state: FSMContext):
    user_data = await state.get_data()
    crud.create_task(
        user_id=message.from_user.id,
        title=user_data['title'],
        deadline=user_data['deadline'],
        category=user_data['category'],
        priority=message.text
    )
    await state.clear()
    await message.answer(
        "Задача успешно добавлена! ✅",
        reply_markup=ReplyKeyboardRemove()
        )

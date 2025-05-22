from aiogram import Router, F
from aiogram.types import Message
from database import crud
from datetime import datetime
from datetime import datetime, timedelta

def get_week_day(task):
    weekday_number = task.deadline.weekday()
    week_days = {
        0: "Понедельник",
        1: "Вторник",
        2: "Среда",
        3: "Четверг",
        4: "Пятница",
        5: "Суббота",
        6: "Воскресенье"
    }
    return week_days[weekday_number]

router = Router()
@router.message(F.text == "/start")
async def start_command(message: Message):
    await message.answer(
        f"Привет, {message.from_user.first_name}! 👋\n"
        "Я помогу тебе управлять задачами. 🎯\n\n"
        "Нажми /help, чтобы посмотреть список доступных команд.",
        parse_mode="HTML"
    )

@router.message(F.text == "/help")
async def help_command(message: Message):
    await message.answer(
        "ℹ️ Доступные команды:\n\n"
        "/start — запускает бота\n"
        "/add — создать новую задачу\n"  
        "/list — показать все задачи\n"  
        "/week_tasks — задачи на неделю\n"  
        "/delete — удалить задачу\n"  
        "/done — отметить как выполненную\n" 
        "/edit — изменить задачу\n"  
        "/remind — установить напоминание\n"
        "/stats — статистика выполнения\n"
        "/help — эта справка"
    )

@router.message(F.text == "/list")
async def list_tasks(message: Message):
    tasks = crud.get_tasks_by_user(user_id=message.from_user.id)
    
    if not tasks:
        await message.answer("📭 У вас пока нет задач.", parse_mode="HTML")
        return

    response = "📌 Ваши задачи:\n\n"
    for idx, task in enumerate(tasks, 1):
        deadline_str = task.deadline.strftime("%d.%m.%Y %H:%M")
        weekday = get_week_day(task)
        status_text = '🟠 В процессе' if task.status == 'pending' else '🟢 Завершена'
        response += (
            f"{idx}. <b>{task.title}</b>\n"
            f" <b>Дедлайн:</b> {deadline_str}  ({weekday})\n"
            f" <b>Категория:</b> {task.category}\n"
            f" <b>Приоритет:</b> {task.priority}\n"
            f" <b>Статус:</b> {status_text}\n"
            "\n"
        )
        
    await message.answer(response, parse_mode="HTML")

@router.message(F.text == "/week_tasks")
async def show_calendar_week(message: Message):
    user_id = message.from_user.id

    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    start_of_week = today - timedelta(days=today.weekday())  
    end_of_week = start_of_week + timedelta(days=6, hours=23, minutes=59, seconds=59)  

    tasks = crud.get_tasks_by_deadline_range(user_id=user_id, start=start_of_week, end=end_of_week)

    if not tasks:
        await message.answer("🎉 У вас нет задач на эту неделю.")
        return

    response = "📅 Вот задачи на эту неделю:\n\n"
    for idx, task in enumerate(tasks, 1):
        deadline_str = task.deadline.strftime("%d.%m %H:%M")
        status_text = '🟠 В процессе' if task.status == 'pending' else '🟢 Завершена'
        response += (
            f"{idx}. <b>{task.title}</b>\n"
            f" <b>Дедлайн:</b> {deadline_str}\n"
            f" <b>Категория:</b> {task.category}\n"
            f" <b>Приоритет:</b> {task.priority}\n"
            f" <b>Статус:</b> {status_text}\n"
            "\n"
        )

    await message.answer(response, parse_mode="HTML")

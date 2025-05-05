from handlers.base_imports import *

router = Router()
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
        status_text = '🟠 В процессе' if task.status == 'pending' else '🟢 Завершена'
        response += (
            f"{idx}. <b>{task.title}</b>\n"
            f" <b>ID:</b> {task.id}\n"
            f" <b>Дедлайн:</b> {deadline_str}\n"
            f" <b>Категория:</b> {task.category}\n"
            f" <b>Приоритет:</b> {task.priority}\n"
            f" <b>Статус:</b> {status_text}\n"
            "———————–———————–———————–———————–\n"
        )
        
    await message.answer(response, parse_mode="HTML")

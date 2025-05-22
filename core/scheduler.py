from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
from database import crud
from aiogram import Bot

scheduler = AsyncIOScheduler()

async def check_reminders(bot: Bot):
    now = datetime.now()
    # получаем все задачи, где deadline - reminder_days == today
    tasks = crud.get_tasks_with_due_reminder(now.date())

    for task in tasks:
        user_id = task.user_id
        message_text = (
            "🔔 Напоминание!\n"
            f"• Задача: <b>{task.title}</b>\n"
            f"• Дедлайн: {task.deadline.strftime('%d.%m.%Y %H:%M')}\n"
            f"• Приоритет: {task.priority}"
        )
        await bot.send_message(user_id, message_text, parse_mode="HTML")
import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import router
from database.models import Base
from database import engine
from scheduler import scheduler, check_reminders

async def main():
    Base.metadata.create_all(bind=engine)

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(router)
    
    scheduler.start()
    scheduler.add_job(check_reminders, 'cron', hour=9, minute=15, args=[bot])

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

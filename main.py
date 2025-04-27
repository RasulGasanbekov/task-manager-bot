import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import tasks
from database.models import Base
from database import engine

async def main():
    Base.metadata.create_all(bind=engine)

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(tasks.router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

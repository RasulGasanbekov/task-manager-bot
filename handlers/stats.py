from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram_calendar import SimpleCalendar, SimpleCalendarCallback
from datetime import datetime, timedelta
from database import crud, SessionLocal
from utils.keyboards import get_category_keyboard, get_priority_keyboard, get_period_keyboard

router = Router()

# === FSM для статистики ===
class StatsFilter(StatesGroup):
    category = State()
    priority = State()
    period = State()
    custom_date_range = State()

# === Календарь ===
calendar = SimpleCalendar()

# === Обработчики команды /stats ===

@router.message(F.text == "/stats")
async def start_stats(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(StatsFilter.category)
    await message.answer("📂 Выберите категорию:", reply_markup=get_category_keyboard())


@router.callback_query(StatsFilter.category)
async def choose_priority(callback: CallbackQuery, state: FSMContext):
    category = callback.data.split("_")[1]
    await state.update_data(category=category)
    await state.set_state(StatsFilter.priority)
    await callback.message.edit_text("🔺 Выберите приоритет:", reply_markup=get_priority_keyboard())


@router.callback_query(StatsFilter.priority)
async def choose_period(callback: CallbackQuery, state: FSMContext):
    priority = callback.data.split("_")[1]
    await state.update_data(priority=priority)
    await state.set_state(StatsFilter.period)
    await callback.message.edit_text("⏳ За какой период посмотреть?", reply_markup=get_period_keyboard())


from datetime import datetime, timedelta
from calendar import monthrange

@router.callback_query(StatsFilter.period, F.data.startswith("period_"))
async def show_stats(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = callback.from_user.id
    category = data.get("category")
    priority = data.get("priority")
    period = callback.data.split("_")[1]

    now = datetime.now()

    # === Определяем период и заголовок для вывода ===
    if period == "today":
        start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = start_date + timedelta(days=1)
        period_title = f"за {start_date.strftime('%d.%m.%Y')}"

    elif period == "week":
        # Начало недели (понедельник)
        start_date = now - timedelta(days=now.weekday())
        end_date = start_date + timedelta(days=7)
        period_title = f"с {start_date.strftime('%d.%m.%Y')} по {end_date.strftime('%d.%m.%Y')}"

    elif period == "month":
        _, days_in_month = monthrange(now.year, now.month)
        start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end_date = now.replace(day=days_in_month, hour=23, minute=59, second=59, microsecond=999999)
        period_title = f"за {now.strftime('%B %Y')}"

    else:
        # Пользователь хочет выбрать свой диапазон
        await state.set_state(StatsFilter.custom_date_range)
        await callback.message.edit_text("📅 Выберите период в календаре", reply_markup=await calendar.start_calendar())
        return

    with SessionLocal() as db:
        tasks = crud.get_tasks_by_filters(
            db=db,
            user_id=user_id,
            category=category,
            priority=priority,
            start=start_date,
            end=end_date
        )

    total = len(tasks)
    completed = sum(1 for t in tasks if t.status == "completed")
    percent = round(completed / total * 100, 1) if total > 0 else 0

    # === Отправляем результат с красивым заголовком ===
    await callback.message.edit_text(
        f"📊 Статистика {period_title}:\n\n"
        f"📌 Всего задач: {total}\n"
        f"✅ Выполнено: {completed}\n"
        f"❌ Не выполнено: {total - completed}\n"
        f"📈 Процент выполнения: {percent}%\n"
    )
    await state.clear()


@router.callback_query(StatsFilter.custom_date_range, SimpleCalendarCallback.filter())
async def process_calendar(
    callback: CallbackQuery,
    callback_data: SimpleCalendarCallback,
    state: FSMContext
):
    selected, date = await calendar.process_selection(callback, callback_data)

    if selected:
        data = await state.get_data()
        category = data.get("category")
        priority = data.get("priority")

        with SessionLocal() as db:
            tasks = crud.get_tasks_by_filters(
                db=db,
                user_id=callback.from_user.id,
                category=category,
                priority=priority,
                start=date,
                end=date + timedelta(days=1)
            )

        total = len(tasks)
        completed = sum(1 for t in tasks if t.status == "completed")
        percent = round(completed / total * 100, 1) if total > 0 else 0

        await callback.message.delete()
        await callback.message.answer(
            f"📊 Статистика за {date.strftime('%d.%m.%Y')}:\n"
            f"📌 Всего задач: {total}\n"
            f"✅ Выполнено: {completed}\n"
            f"❌ Не выполнено: {total - completed}\n"
            f"📈 Процент выполнения: {percent}%"
        )
        await state.clear()
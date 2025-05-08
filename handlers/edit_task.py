from .base_imports import *

router = Router()

class EditTask(StatesGroup):
    task_id = State()
    title = State()
    deadline = State()
    category = State()
    priority = State()

@router.message(F.text.startswith("/edit"))
async def edit_task_start(message: Message, state: FSMContext):
    text = message.text.strip()
    parts = text.split()

    if len(parts) < 2:
        await message.answer("❌ Укажите ID задачи. Пример: <code>/edit 1</code>", parse_mode="HTML")
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

    await state.update_data(task_id=task_id)
    await state.set_state(EditTask.title)

    await message.answer(f"📝 Введите новое название задачи (было: <b>{task.title}</b>):", parse_mode="HTML")

@router.message(EditTask.title)
async def edit_task_deadline(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(EditTask.deadline)
    await message.answer("📅 Укажите новый дедлайн (формат ДД.ММ.ГГГГ ЧЧ:ММ):")


@router.message(EditTask.deadline)
async def edit_task_category(message: Message, state: FSMContext):
    try:
        deadline = datetime.strptime(message.text, "%d.%m.%Y %H:%M")
        await state.update_data(deadline=deadline)
        await state.set_state(EditTask.category)
        await message.answer("📁 Выберите новую категорию:", reply_markup=keyboards.category_keyboard())
    except ValueError:
        await message.answer("⚠️ Неверный формат даты. Используйте: ДД.ММ.ГГГГ ЧЧ:ММ")


@router.message(EditTask.category)
async def edit_task_priority(message: Message, state: FSMContext):
    await state.update_data(category=message.text)
    await state.set_state(EditTask.priority)
    await message.answer("🔺 Выберите новый приоритет:", reply_markup=keyboards.priority_keyboard())


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
        status = 'pending'
    )

    await state.clear()
    await message.answer("✅ Задача успешно обновлена!", reply_markup=ReplyKeyboardRemove())
from handlers.base_imports import *

router = Router()

class AddTask(StatesGroup):
    title = State()
    deadline = State()
    category = State()
    priority = State()

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
    await state.update_data(category=message.text.lower())
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
        priority=message.text.lower()
    )
    await state.clear()
    await message.answer(
        "Задача успешно добавлена! ✅",
        reply_markup=ReplyKeyboardRemove()
    )
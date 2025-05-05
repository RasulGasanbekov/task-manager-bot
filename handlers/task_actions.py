from handlers.base_imports import *

router = Router()
@router.message(F.text.startswith("/delete"))
async def delete_task(message: Message):
    text = message.text.strip()  
    parts = text.split()  

    if len(parts) < 2:
        await message.answer("❌ Укажите ID задачи. Пример: <code>/delete 1</code>", parse_mode="HTML")
        return
    
    try:
        task_id = int(parts[1])
    except ValueError:
        await message.answer("❌ Неверный формат ID. Пожалуйста, введите целое число.")
        return
    
    task = crud.get_task_by_id(user_id=message.from_user.id, task_id=task_id)
    
    if not task:
        await message.answer(f"❌ Задача с ID {task_id} не найдена.")
        return
    
    crud.delete_task(task_id=task_id)
    
    await message.answer(f"🗑️ Задача \"{task.title}\" успешно удалена!")

@router.message(F.text.startswith("/done"))
async def mark_task_done(message: Message):
    text = message.text.strip()  
    parts = text.split()  

    if len(parts) < 2:
        await message.answer("❌ Укажите ID задачи. Пример: <code>/done 1</code>", parse_mode="HTML")
        return
    
    try:
        task_id = int(parts[1])
    except ValueError:
        await message.answer("❌ Неверный формат ID. Пожалуйста, введите целое число.")
        return
    
    task = crud.get_task_by_id(user_id=message.from_user.id, task_id=task_id)
    
    if not task:
        await message.answer(f"❌ Задача с ID {task_id} не найдена.")
        return
    
    crud.update_task_status(task_id=task_id, new_status="completed")
    
    await message.answer(f"🎉 Задача \"{task.title}\" успешно помечена как выполненная!")
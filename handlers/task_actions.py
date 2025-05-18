from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from handlers.task_selector import start_task_selection

router = Router()

@router.message(F.text == "/delete")
async def delete_task_command(message: Message, state: FSMContext):
    await start_task_selection(message, state, "delete")

@router.message(F.text == "/done")
async def mark_task_done_command(message: Message, state: FSMContext):
    await start_task_selection(message, state, "done")

@router.message(F.text == "/edit")
async def edit_task_command(message: Message, state: FSMContext):
    await start_task_selection(message, state, "edit")

@router.message(F.text == "/remind")
async def edit_task_command(message: Message, state: FSMContext):
    await start_task_selection(message, state, "remind")
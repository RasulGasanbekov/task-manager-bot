from .common_commands import router as common_router
from .add_task import router as add_task_router
from .task_actions import router as task_actions_router
from .edit_task import router as edit_task_router

router = common_router  

router.include_router(add_task_router)
router.include_router(task_actions_router)
router.include_router(edit_task_router)
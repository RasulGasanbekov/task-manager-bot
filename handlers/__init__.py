from .common_commands import router as common_router
from .add_task import router as add_task_router
from .task_actions import router as task_actions_router
from .task_selector import router as task_selector_router
from .edit_task import router as edit_task_router
from .stats import router as stats_router
from .remind import router as remind_router

router = common_router

router.include_router(add_task_router)
router.include_router(task_actions_router)
router.include_router(task_selector_router)
router.include_router(edit_task_router)
router.include_router(remind_router)
router.include_router(stats_router)

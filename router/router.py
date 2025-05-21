from aiogram import Router

from handlers.admins.admins_actions import router as admins_actions_router
from handlers.admins.event_actions import router as event_actions_router
from handlers.admins.main_menu import router as main_menu_router
from handlers.admins.report_actions import router as report_actions_router
from handlers.chating import router as chating_router
from handlers.commands import router as commands_router
from handlers.users import router as users_router

router = Router()

router.include_routers(
    commands_router,
    users_router,
    main_menu_router,
    admins_actions_router,
    event_actions_router,
    report_actions_router,
    chating_router
)

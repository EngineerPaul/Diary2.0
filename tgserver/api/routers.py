from fastapi import APIRouter

from api.api import router as reminders_router

main_router = APIRouter(prefix='/tgapi')
main_router.include_router(reminders_router)

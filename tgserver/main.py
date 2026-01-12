from fastapi import FastAPI
import uvicorn

from api.routers import main_router
from dependencies import set_session, close_session


app = FastAPI()
app.include_router(main_router)

@app.on_event("startup")
async def startup_event():
    await set_session()

@app.on_event("shutdown")
async def shutdown_event():
    await close_session()


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True, host='0.0.0.0')

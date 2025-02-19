import uvicorn
import os
from fastapi import FastAPI
from containers import Container
from user.interface.controllers.user_controller import router as user_router
from screenshot.interface.controllers.screenshot_controller import router as screenshot_router
from notification.interface.controllers.notification_controller import router as notification_router
from category.interface.controllers.category_controller import router as category_router

from contextlib import asynccontextmanager

from notification_worker import check_and_send_notifications
from utils.logger import logger


def create_temp_directory():
    if not os.path.exists("temp"):
        os.makedirs("temp")

create_temp_directory()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await check_and_send_notifications()
    yield


app = FastAPI(lifespan=lifespan)
app.container = Container()
app.include_router(user_router)
app.include_router(screenshot_router)
app.include_router(notification_router)
app.include_router(category_router)

@app.get("/")
def hello():
    logger.debug("debug: Hello World")
    return {"Hello": "World"}

log_config = uvicorn.config.LOGGING_CONFIG
log_config["formatters"]["access"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
log_config["formatters"]["default"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_config=log_config)

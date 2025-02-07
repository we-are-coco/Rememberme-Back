import uvicorn
import os
from fastapi import FastAPI
from containers import Container
from user.interface.controllers.user_controller import router as user_router
from screenshot.interface.controllers.screenshot_controller import router as screenshot_router
from notification.interface.controllers.notification_controller import router as notification_router

def create_temp_directory():
    if not os.path.exists("temp"):
        os.makedirs("temp")

create_temp_directory()

app = FastAPI()
app.container = Container()
app.include_router(user_router)
app.include_router(screenshot_router)
app.include_router(notification_router)

@app.get("/")
def hello():
    return {"Hello": "World"}

log_config = uvicorn.config.LOGGING_CONFIG
log_config["formatters"]["access"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
log_config["formatters"]["default"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
uvicorn.run(app, host="0.0.0.0", port=8000, log_config=log_config)

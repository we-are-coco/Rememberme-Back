from fastapi import FastAPI
from containers import Container
from user.interface.controllers.user_controller import router as user_router
from screenshot.interface.controllers.screenshot_controller import router as screenshot_router

app = FastAPI()
app.container = Container()
app.include_router(user_router)
app.include_router(screenshot_router)

@app.get("/")
def hello():
    return {"Hello": "World"}

from fastapi import FastAPI
from app.api.router import api_router

import uvicorn
from contextlib import asynccontextmanager

from app.services.video_processor import CameraService

import RPi.GPIO as GPIO

# from app.services.relay_control import RelayService

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.camera = CameraService()
    
    # self.relay = RelayService(pin=17)
    # self.last_relay_state = False
    
    yield
    app.state.camera.stop()
    GPIO.cleanup()
    print("App shutting down")

app = FastAPI(
    title="Helmet Detection",
    version="1.0.0",
    description="Helmet detection.",
    lifespan=lifespan,
)


app.include_router(api_router)


@app.get("/")
def read_root():
    return {"message": "Helmet detection. Access control interface at /control"}


if __name__ == "__main__":
    # uvicorn.run("app.main:app", port=8000, reload=True)
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)
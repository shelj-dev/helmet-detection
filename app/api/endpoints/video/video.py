from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
import time


router = APIRouter()


@router.get("/video_feed")
def video_feed(request: Request):
    camera = request.app.state.camera

    def generate():
        while True:
            frame = camera.get_frame()
            if frame:
                yield (
                    b"--frame\r\n"
                    b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
                )
            time.sleep(0.03)

    return StreamingResponse(
        generate(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )
    
    
@router.get("/helmet_status")
def helmet_status(request: Request):
    camera_service = request.app.state.camera
    return {"helmet_detected": camera_service.get_helmet_status()}


# @router.get("/bypass_relay_always_on")
# def bypass_relay_always_on(request: Request):
#     camera_service = request.app.state.camera
#     return {"helmet_detected": camera_service.bypass_relay_always_on()}
    
# @router.get("/bypass_relay_always_off")
# def bypass_relay_always_off(request: Request):
#     camera_service = request.app.state.camera
#     return {"helmet_detected": camera_service.bypass_relay_always_off()}
    
# @router.get("/disable_bypass")
# def disable_bypass(request: Request):
#     camera_service = request.app.state.camera
#     return {"helmet_detected": camera_service.disable_bypass()}


@router.post("/bypass_relay_always_on")
def bypass_on():
    camera_service = request.app.state.camera
    camera_service.bypass_relay_always_on()
    return {"status": "ok"}

@router.post("/bypass_relay_always_off")
def bypass_off():
    camera_service = request.app.state.camera
    camera_service.bypass_relay_always_off()
    return {"status": "ok"}

@router.post("/disable_bypass")
def disable():
    camera_service = request.app.state.camera
    camera_service.disable_bypass()
    return {"status": "ok"}
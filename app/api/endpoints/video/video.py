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
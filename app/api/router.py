from fastapi import APIRouter
from app.api.endpoints.video import video
from fastapi.responses import HTMLResponse


api_router = APIRouter()


@api_router.get("/control", response_class=HTMLResponse, tags=["interface"])
async def control_page():
    """Serves the main HTML control page."""
    try:
        with open("static/control.html", "r") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content, status_code=200)
    except FileNotFoundError:
        return HTMLResponse(
            content="<h1>Error: static/control.html not found!</h1>", status_code=404
        )

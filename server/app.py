
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from server.routes import endpoints, events, songs, users, admin, user_features

app = FastAPI(
    title="ZazMusic API",
    version="1.0.0",
    description="Backend API for ZazMusic"
)


@app.get("/")
def home():
    return {
        "message": "ZazMusic API is running"
    }


# Register routers
app.include_router(endpoints.router)
app.include_router(events.router)
app.include_router(user_features.router)
app.include_router(songs.router)
app.include_router(users.router)
app.include_router(admin.router)

# Serve the web client from the same origin as the API. Open /app after
# starting the backend to avoid browser CORS issues during local development.
FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"
if FRONTEND_DIR.exists():
    app.mount("/app", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")

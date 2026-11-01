
from fastapi import FastAPI

from server.routes import endpoints, events, songs, users, admin

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
app.include_router(songs.router)
app.include_router(users.router)
app.include_router(admin.router)

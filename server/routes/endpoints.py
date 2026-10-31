
from fastapi import APIRouter

router = APIRouter(
    prefix="/endpoints",
    tags=["Endpoints"]
)


@router.get("/")
def get_endpoints():
    return {
        "message": "Endpoints API is working"
    }

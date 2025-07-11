from fastapi import APIRouter



hr_router = APIRouter()



@hr_router.get("/health")
async def health_check():
    return {
        "status_code": 200,
        "message": "Server is up and Running!"
    }
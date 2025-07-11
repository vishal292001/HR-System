# main.py
from fastapi import FastAPI, HTTPException, Depends, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from app.router import hr_router
from app.middleware import RateLimitMiddleware

# Initialize FastAPI app
app = FastAPI(
    title="HR Employee Search API",
    description="Employee search directory API for HR companies",
    version="1.0.0",
    docs_url='/docs'
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(RateLimitMiddleware)
app.include_router(hr_router)



# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
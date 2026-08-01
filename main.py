from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import traceback
from routers.routers.cities import router as cities_router
from routers.routers.categories import router as categories_router
from routers.routers.reports import router as reports_router
from routers.routers.auth import router as auth_router
from routers.routers import statistics


import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Fix Georgia API"
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    traceback.print_exc()

    return JSONResponse(
        status_code=500,
        content={
            "message": "Internal Server Error",
            "error": str(exc)
        }
    )



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)





app.include_router(
    statistics.router
)


app.include_router(
    auth_router
)


app.include_router(
    cities_router
)


app.include_router(
    categories_router
)


app.include_router(
    reports_router
)



# ROOT

@app.get("/")
def home():

    return {
        "message": "Fix Georgia API running"
    }
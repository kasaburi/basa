from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.routers.cities import router as cities_router
from routers.routers.categories import router as categories_router
from routers.routers.reports import router as reports_router
from routers.routers.auth import router as auth_router
from routers.routers import statistics



app = FastAPI(
    title="Fix Georgia API"
)



# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",
        "http://localhost:50873",
        
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ROUTERS

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
from fastapi import FastAPI
from data.connection import database as database
from fastapi.middleware.cors import CORSMiddleware

from routers import (
    students,
    professors,
    clases,
    inscriptions,
    courses,
    levels,
    users,
    discounts,
)

app = FastAPI()

routers = [
    students.router,
    professors.router,
    clases.router,
    inscriptions.router,
    courses.router,
    levels.router,
    users.router,
    discounts.router,
]

for router in routers:
    app.include_router(router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

from fastapi import FastAPI
from routers.students import router as students
from routers.professors import router as professors
from routers.levels import router as levels
from data.connection import database as database


app = FastAPI()
app.include_router(students)
app.include_router(professors)
app.include_router(levels)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

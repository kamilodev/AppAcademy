from fastapi import FastAPI, Response, status
from routers.students import router as students
from routers.professors import router as professors
from connection import database as database


app = FastAPI()
app.include_router(students)
app.include_router(professors)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

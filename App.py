from fastapi import FastAPI
from routers.students import router as students
from routers.professors import router as professors
from routers.clases import router as clases
from data.connection import database as database


app = FastAPI()
app.include_router(students)
app.include_router(professors)
app.include_router(clases)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

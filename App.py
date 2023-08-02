from fastapi import FastAPI
from routers.students import router as students
from routers.professors import router as professors
from routers.clases import router as clases
from routers.inscriptions import router as inscriptions
from routers.courses import router as courses
from routers.levels import router as levels
from routers.users import router as users
from routers.discounts import router as discounts
from data.connection import database as database


app = FastAPI()
app.include_router(students)
app.include_router(professors)
app.include_router(clases)
app.include_router(courses)
app.include_router(levels)
app.include_router(users)
app.include_router(inscriptions)
app.include_router(discounts)



@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

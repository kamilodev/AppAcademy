#!/usr/bin/env python
from fastapi import FastAPI, Response, status
from dotenv import load_dotenv
from Models import Student
from routers.post_students import router as post_students
import databases
import os

load_dotenv(override=True)

app = FastAPI()
app.include_router(post_students)
database = databases.Database(os.environ["MYSQL_ADDON_URI"])
print(os.environ["MYSQL_ADDON_URI"])


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get(
    "/",
    tags=["Students"],
    summary="Get all students",
    response_description="All students in database shown",
)
async def first_api():
    """
    This endpoint allows you to get all students in the database.
    """
    query = "SELECT * FROM students"
    results = await database.fetch_all(query)
    return {"message": "All students", "data": results}


@app.get(
    "/students/{id_students}",
    status_code=status.HTTP_200_OK,
    tags=["Students"],
    summary="Get a student by id",
)
async def get_student(id_students: int, response: Response):
    """
    This endpoint allows you to get a student by id.

    - **id**: DNI of the student (mandatory)
    """
    query = f"SELECT * FROM students WHERE id_students = {id_students}"
    results = await database.fetch_all(query)
    if len(results) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"Student with id: {id_students} not found"
    else:
        response.status_code = status.HTTP_200_OK
        return {"message": "Student found", "data": results[0]}


@app.delete(
    "/students/{id_students}",
    status_code=status.HTTP_200_OK,
    tags=["Delete", "Students"],
    summary="Delete a student by id",
)
async def delete_student(id_students: int, response: Response):
    """
    This endpoint allows you to delete a student by id.

    - **id**: DNI of the student (mandatory)
    """

    query = f"SELECT * FROM students WHERE id_students = {id_students}"
    results = await database.fetch_all(query)
    if len(results) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"Student with id: {id_students} not found"

    delete_query = f"DELETE FROM students WHERE id_students = {id_students}"
    await database.execute(delete_query)

    response.status_code = status.HTTP_200_OK
    return {"message": "Student deleted"}

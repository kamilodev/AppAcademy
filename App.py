#!/usr/bin/env python
from fastapi import FastAPI, Response, status
from dotenv import load_dotenv
from Models import Student
import databases
import os

load_dotenv(override=True)

app = FastAPI()
database = databases.Database(os.environ["MYSQL_ADDON_URI"])
print(os.environ["MYSQL_ADDON_URI"])


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.post("/students", tags=["Create", "Students"], summary="Create a new student")
async def create_student(student: Student):
    """
    This endpoint allows you to create a new student in the database.

    - **id**: DNI of the student (mandatory)
    - **first_name**: First name of the student (mandatory)
    - **last_name**: Last name of the student (mandatory)
    - **phone**: Phone number of the student (mandatory)
    - **email**: Email of the student (mandatory)
    - **age**: Age of the student (mandatory)
    - **id_familiar**: DNI of the familiar (optional)
    """
    query = f"INSERT INTO students (id_students, first_name, last_name, phone, email, age, id_familiar) VALUES (:id_students, :first_name, :last_name, :phone, :email, :age, :id_familiar)"
    values = {
        "id_students": student.id_students,
        "first_name": student.first_name,
        "last_name": student.last_name,
        "phone": student.phone,
        "email": student.email,
        "age": student.age,
        "id_familiar": student.id_familiar,
    }
    await database.execute(query=query, values=values)

    return {"message": "Student created successfully"}


@app.get(
    "/",
    tags=["Read", "Students"],
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
    tags=["Read", "Students"],
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

from fastapi import APIRouter, Response, status
from Models import Student
from connection import database as database

router = APIRouter(prefix="/students", tags=["Students"])


@router.post("/", summary="Create a new student")
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

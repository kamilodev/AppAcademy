from fastapi import APIRouter, Response, status
from Models import Student
from connection import database as database

router = APIRouter(prefix="/students", tags=["Students"])


async def get_student_by_id(id_students: int):
    query = f"SELECT * FROM students WHERE id_students = {id_students}"
    results = await database.fetch_all(query)
    return results


@router.get(
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


@router.get(
    "/{id_students}",
    status_code=status.HTTP_200_OK,
    tags=["Students"],
    summary="Get a student by id",
)
async def get_student(id_students: int, response: Response):
    """
    This endpoint allows you to get a student by id.

    - **id**: DNI of the student (mandatory)
    """
    results = await get_student_by_id(id_students)

    if len(results) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"Student with id: {id_students} not found"
    else:
        response.status_code = status.HTTP_200_OK
        return {"message": "Student found", "data": results[0]}


@router.post("/create/", summary="Create a new student")
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


@router.put("/update/", summary="Update a student")
async def update_student(student: Student, response: Response):
    """
    This endpoint allows you to update the information of a student in the database.

    - **id**: DNI of the student (mandatory)
    - **first_name**: First name of the student (optional)
    - **last_name**: Last name of the student (optional)
    - **phone**: Phone number of the student (optional)
    - **email**: Email of the student (optional)
    - **age**: Age of the student (optional)
    - **id_familiar**: DNI of the familiar (optional)
    """
    results = await get_student_by_id(student.id_students)

    if len(results) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"Student with id: {student.id_students} not found"

    query = f"UPDATE students SET first_name = :first_name, last_name = :last_name, phone = :phone, email = :email, age = :age, id_familiar = :id_familiar WHERE id_students = :id_students"
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

    return f"Student with id {student.id_students} updated successfully"


@router.delete(
    "/delete/{id_students}",
    status_code=status.HTTP_200_OK,
    tags=["Students"],
    summary="Delete a student by id",
)
async def delete_student(id_students: int, response: Response):
    """
    This endpoint allows you to delete a student by id.

    - **id**: DNI of the student (mandatory)
    """
    results = await get_student_by_id(id_students)

    if len(results) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"Student with id: {id_students} not found"

    delete_query = f"DELETE FROM students WHERE id_students = {id_students}"
    await database.execute(delete_query)

    response.status_code = status.HTTP_200_OK
    return f"Student with id {id_students} deleted"

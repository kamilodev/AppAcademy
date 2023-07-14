from data.connection import database as database
from fastapi import status, Response
from data.Models import Student


async def get_student_by_id(id_students: int):
    query = f"SELECT * FROM students WHERE id_students = {id_students}"
    results = await database.fetch_all(query)
    return results


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


async def get_all_students():
    """
    This endpoint allows you to get all students in the database.
    """
    query = "SELECT * FROM students"
    results = await database.fetch_all(query)
    return {"message": "All students", "data": results}


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


# TODO: Validate if familiar exists
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

    update_fields = {}

    if student.first_name != "string":
        update_fields["first_name"] = student.first_name
    if student.last_name != "string":
        update_fields["last_name"] = student.last_name
    if student.phone != "string":
        update_fields["phone"] = student.phone
    if student.email != "string":
        update_fields["email"] = student.email
    if student.age != 0:
        update_fields["age"] = student.age
    if student.id_familiar != 0:
        update_fields["id_familiar"] = student.id_familiar

    if len(update_fields) == 0:
        return f"No fields to update for student with id: {student.id_students}"

    set_query = ", ".join(f"{field} = :{field}" for field in update_fields)
    values = {"id_students": student.id_students, **update_fields}

    query = f"UPDATE students SET {set_query} WHERE id_students = :id_students"
    await database.execute(query=query, values=values)

    return f"Student with id {student.id_students} updated successfully"


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

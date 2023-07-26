import json
from data.connection import database as database
from data.Models import DeleteStudent, Student, UpdateStudent
from fastapi import status, Response, HTTPException
from typing import List


async def get_student_by_id(id_students: str):
    query = f"SELECT * FROM students WHERE id_students = :id_students"
    values = {"id_students": id_students}
    results = await database.fetch_all(query, values)
    return results


async def change_familiar_discount(id_familiar: str):
    from controllers import inscriptions

    familiar_students = await get_student_by_id(id_familiar)
    is_active = await inscriptions.get_active_inscriptions_by_student(id_familiar)

    if len(is_active) > 0:
        id_inscription = is_active[0]["id_inscriptions"]
        print(id_inscription)


async def get_student(id_students: str, response: Response):
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


async def get_all_students(response: Response):
    """
    This endpoint allows you to get all students in the database.
    """
    query = "SELECT * FROM students ORDER BY id_students ASC"
    results = await database.fetch_all(query)
    if len(results) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"No students found"
    return {"message": "All students", "data": results}


# TODO: Validar si el descuento del 10% se aplica a ambos familiares, o solo al familiar que se inscribe
async def create_student(student: Student, response: Response):
    """
    This endpoint allows you to create a new student in the database.

    - **id**: DNI of the student (mandatory)
    - **first_name**: First name of the student (mandatory)
    - **last_name**: Last name of the student (mandatory)
    - **phone**: Phone number of the student (mandatory)
    - **email**: Email of the student (mandatory)
    - **age**: Age of the student (mandatory)
    - **id_familiar**: DNI of the familiar (optional)
    - **status**: Status of the student
    """
    default_values = ["string", "", 0]

    for field in student.__fields__:
        if student.__getattribute__(field) in default_values:
            if field == "id_familiar" or field == "status":
                continue
            else:
                response.status_code = status.HTTP_400_BAD_REQUEST
                return f"Field {field} cannot be empty"

    familiar_id = student.id_familiar
    if familiar_id != "string" and familiar_id != "0" and len(familiar_id) > 0:
        result = await get_student_by_id(familiar_id)
        if len(result) == 0:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return f"Familiar with id: {familiar_id} not found"
    else:
        familiar_id = "0"

    query = f"INSERT INTO students (id_students, first_name, last_name, phone, email, age, id_familiar, status, familiar) VALUES (:id_students, :first_name, :last_name, :phone, :email, :age, :id_familiar, :status, :familiar)"
    values = {
        "id_students": student.id_students,
        "first_name": student.first_name,
        "last_name": student.last_name,
        "phone": student.phone,
        "email": student.email,
        "age": student.age,
        "id_familiar": "0",
        "status": student.status,
        "familiar": familiar_id,
    }

    duplicate_student = await get_student_by_id(student.id_students)
    if len(duplicate_student) > 0:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return f"Student with id: {student.id_students} already exists"

    await database.execute(query=query, values=values)

    if familiar_id != "string" and familiar_id != "0" and len(familiar_id) > 0:
        familiar_query = f"UPDATE students SET id_familiar = JSON_ARRAY_APPEND(id_familiar, '$', :new_familiar) WHERE id_students = :familiar_id"
        familiar_values = {
            "new_familiar": student.id_students,
            "familiar_id": familiar_id,
        }
        await database.execute(query=familiar_query, values=familiar_values)

    return {"message": "Student created successfully"}


async def update_student(student: UpdateStudent, response: Response):
    """
    This endpoint allows you to update the information of a student in the database.

    - **id**: DNI of the student (mandatory)
    - **first_name**: First name of the student (optional)
    - **last_name**: Last name of the student (optional)
    - **phone**: Phone number of the student (optional)
    - **email**: Email of the student (optional)
    - **age**: Age of the student (optional)
    - **id_familiar**: DNI of the familiar (optional)
    - **status**: Status of the student
    """
    from controllers import inscriptions

    results = await get_student_by_id(student.id_students)

    if student.id_students == "" or student.id_students == "string":
        response.status_code = status.HTTP_400_BAD_REQUEST
        return f"Student id cannot be empty"

    if len(results) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"Student with id: {student.id_students} not found"

    existing_student = results[0]

    if existing_student["status"] == 1 and student.status == 0:
        active_inscriptions = await inscriptions.get_active_inscriptions_by_student(
            student.id_students
        )

        if len(active_inscriptions) > 0:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return f"Student with id: {student.id_students} has active inscriptions and cannot be deactivated"

    update_fields = {}
    default_values = {
        "first_name": "string",
        "last_name": "string",
        "phone": "string",
        "email": "string",
        "age": 0,
    }

    for field in student.__fields__:
        if field == "id_students":
            continue
        if field == "status":
            if student.__getattribute__(field) != existing_student[field]:
                update_fields[field] = student.__getattribute__(field)
        elif student.__getattribute__(field) != default_values[field]:
            update_fields[field] = student.__getattribute__(field)

    if len(update_fields) == 0:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return f"No fields to update for student with id: {student.id_students}"

    set_query = ", ".join(f"{field} = :{field}" for field in update_fields)
    values = {"id_students": student.id_students, **update_fields}

    query = f"UPDATE students SET {set_query} WHERE id_students = :id_students"
    await database.execute(query=query, values=values)

    return f"Student with id {student.id_students} updated successfully"


async def delete_student(student: DeleteStudent, response: Response):
    """
    This endpoint allows you to delete a student by id.

    - **id**: DNI of the student (mandatory)
    """
    from controllers import inscriptions

    results = await get_student_by_id(student.id_students)

    if student.id_students == "" or student.id_students == "string":
        response.status_code = status.HTTP_400_BAD_REQUEST
        return f"Student id cannot be empty"

    if len(results) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"Student with id: {student.id_students} not found"

    result = await inscriptions.get_active_inscriptions_by_student(student.id_students)
    if len(result) > 0:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return f"Student with id: {student.id_students} has active inscriptions"

    response.status_code = status.HTTP_200_OK
    query = f"UPDATE students SET status = '0' WHERE id_students = :id_students"
    await database.execute(query=query, values={"id_students": student.id_students})
    return f"Student with id {student.id_students} is now inactive"

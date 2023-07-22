from data.connection import database as database
from data.Models import DeleteStudent, Student
from fastapi import status, Response, HTTPException


async def get_student_by_id(id_students: str):
    query = f"SELECT * FROM students WHERE id_students = :id_students"
    values = {"id_students": id_students}
    results = await database.fetch_all(query, values)
    return results


async def get_familiar_id(student_id: str, response: Response) -> str:
    """
    This function checks if the provided student_id is a valid familiar ID.
    If the student_id is valid and corresponds to an existing student, it returns the ID.
    If the student_id is not valid or does not correspond to any existing student, it returns "0".
    """
    if student_id != "string" and student_id != "0" and len(student_id) > 0:
        result = await get_student_by_id(student_id)
        if len(result) == 0:
            response.status_code = status.HTTP_400_BAD_REQUEST
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Familiar with id: {student_id} not found",
            )
        return student_id
    return "0"


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

    student.id_familiar = await get_familiar_id(student.id_familiar, response)

    query = f"INSERT INTO students (id_students, first_name, last_name, phone, email, age, id_familiar, status) VALUES (:id_students, :first_name, :last_name, :phone, :email, :age, :id_familiar, :status)"
    values = {
        "id_students": student.id_students,
        "first_name": student.first_name,
        "last_name": student.last_name,
        "phone": student.phone,
        "email": student.email,
        "age": student.age,
        "id_familiar": student.id_familiar,
        "status": student.status,
    }

    duplicate_student = await get_student_by_id(student.id_students)
    if len(duplicate_student) > 0:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return f"Student with id: {student.id_students} already exists"

    await database.execute(query=query, values=values)

    return {"message": "Student created successfully"}


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
    - **status**: Status of the student
    """
    results = await get_student_by_id(student.id_students)

    if student.id_students == "" or student.id_students == "string":
        response.status_code = status.HTTP_400_BAD_REQUEST
        return f"Student id cannot be empty"

    if len(results) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"Student with id: {student.id_students} not found"

    existing_student = results[0]

    update_fields = {}
    default_values = {
        "first_name": "string",
        "last_name": "string",
        "phone": "string",
        "email": "string",
        "age": 0,
        "id_familiar": "string",
    }

    for field in student.__fields__:
        if field == "id_students":
            continue
        if field == "status":
            if student.__getattribute__(field) != existing_student[field]:
                update_fields[field] = student.__getattribute__(field)
        elif student.__getattribute__(field) != default_values[field]:
            update_fields[field] = student.__getattribute__(field)

    if student.id_familiar != "string":
        update_fields["id_familiar"] = await get_familiar_id(
            student.id_familiar, response
        )

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

    result = await inscriptions.get_inscription_by_student(student.id_students)
    if len(result) > 0:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return f"Student with id: {student.id_students} has active inscriptions"

    response.status_code = status.HTTP_200_OK
    query = f"UPDATE students SET status = '0' WHERE id_students = :id_students"
    await database.execute(query=query, values={"id_students": student.id_students})
    return f"Student with id {student.id_students} is now inactive"

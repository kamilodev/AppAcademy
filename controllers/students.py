import controllers.auxiliar_functions
from data.connection import database as database
from data.Models import DeleteStudent, Student, UpdateStudent
from fastapi import status, Response


async def get_student_by_id(id_students: str):
    """
    The function `get_student_by_id` retrieves student information from a database based on their ID.

    :param id_students: The parameter `id_students` is a string that represents the ID of a student. It
    is used as a filter in the SQL query to retrieve the student with the matching ID from the
    `students` table in the database
    :type id_students: str
    :return: the results of a database query.
    """
    query = "SELECT * FROM students WHERE id_students = :id_students"
    values = {"id_students": id_students}
    try:
        return await database.fetch_all(query, values)
    except Exception as e:
        print(f"Error in get_student_by_id: {e}")
        return []


async def get_student(id_students: str, response: Response):
    """
    This endpoint allows you to get a student by id.

    - **id**: DNI of the student (mandatory)
    """
    results = await get_student_by_id(id_students)

    if not results:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"Student with id: {id_students} not found"
    response.status_code = status.HTTP_200_OK
    return {"message": "Student found", "data": results[0]}


async def get_all_students(response: Response):
    """
    This endpoint allows you to get all students in the database.
    """
    query = "SELECT * FROM students ORDER BY id_students ASC"
    try:
        results = await database.fetch_all(query)
        if not results:
            response.status_code = status.HTTP_404_NOT_FOUND
            return "No students found"
        return {"message": "All students", "data": results}
    except Exception as e:
        if response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
            return f"Internal server error: {e}"


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

    for field in Student.__fields__.keys():
        if student.__getattribute__(field) in default_values:
            if field in ["id_familiar", "status"]:
                continue
            response.status_code = status.HTTP_400_BAD_REQUEST
            return f"Field {field} cannot be empty"

    familiar_id = student.id_familiar
    if familiar_id not in ["string", "0"] and familiar_id:
        result = await get_student_by_id(familiar_id)
        if not result:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return f"Familiar with id: {familiar_id} not found"
    else:
        familiar_id = "0"

    query = "INSERT INTO students (id_students, first_name, last_name, phone, email, age, id_familiar, status, familiar) VALUES (:id_students, :first_name, :last_name, :phone, :email, :age, :id_familiar, :status, :familiar)"
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

    if await get_student_by_id(student.id_students):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return f"Student with id: {student.id_students} already exists"

    await database.execute(query=query, values=values)

    if familiar_id not in ["string", "0"] and familiar_id:
        familiar_query = "UPDATE students SET id_familiar = JSON_ARRAY_APPEND(id_familiar, '$', :new_familiar) WHERE id_students = :familiar_id"
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

    results = await get_student_by_id(student.id_students)

    if student.id_students in ["", "string"]:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return "Student id cannot be empty"

    if not results:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"Student with id: {student.id_students} not found"

    existing_student = results[0]

    if existing_student["status"] == 1 and student.status == 0:
        active_inscriptions = (
            await controllers.auxiliar_functions.get_active_inscriptions_by_student(
                student.id_students
            )
        )

        if active_inscriptions:
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

    if not update_fields:
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

    results = await get_student_by_id(student.id_students)

    if student.id_students in ["", "string"]:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return "Student id cannot be empty"

    if not results:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"Student with id: {student.id_students} not found"

    result = await controllers.auxiliar_functions.get_active_inscriptions_by_student(
        student.id_students
    )
    if result:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return f"Student with id: {student.id_students} has active inscriptions"

    response.status_code = status.HTTP_200_OK
    query = "UPDATE students SET status = '0' WHERE id_students = :id_students"
    await database.execute(query=query, values={"id_students": student.id_students})
    return f"Student with id {student.id_students} is now inactive"

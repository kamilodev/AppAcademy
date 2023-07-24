from typing import List, Optional
from controllers.courses import get_courses_by_id
from controllers.students import get_student_by_id
from data.Models import Inscription, InscriptionDetail, UpdateInscription
from data.connection import database as database
from fastapi import status, Response, Query
from datetime import datetime


master_query = "SELECT inscriptions.id_inscriptions AS id_inscriptions,inscriptions.date_inscription AS date_inscription,students.id_students AS id_student,students.first_name AS first_name,students.last_name AS last_name,students.phone AS phone,courses.id_courses AS id_courses,classes.name AS class_name,levels.name AS level_name,professors.first_name AS professor_first_name,professors.last_name AS professor_last_name,inscriptions.observation AS observation,inscriptions_detail.unit_price AS unit_price,inscriptions_detail.aply_discount AS aply_discount,inscriptions_detail.status AS status FROM inscriptions INNER JOIN students ON inscriptions.id_students = students.id_students INNER JOIN inscriptions_detail ON inscriptions.id_inscriptions = inscriptions_detail.id_inscriptions INNER JOIN courses ON inscriptions_detail.id_courses = courses.id_courses INNER JOIN classes ON courses.id_classes = classes.id_classes INNER JOIN levels ON courses.id_levels = levels.id_levels INNER JOIN professors ON courses.id_professors = professors.id_professors"


async def check_course_in_inscription(id_inscription: int, id_course: int) -> bool:
    query = "SELECT id_inscriptions FROM inscriptions_detail WHERE id_inscriptions = :id_inscription AND id_courses = :id_course"
    values = {"id_inscription": id_inscription, "id_course": id_course}
    result = await database.fetch_all(query, values)
    return len(result) > 0


async def get_inscription_by_id(id_inscriptions: int):
    query = f"SELECT * FROM inscriptions WHERE id_inscriptions = :id_inscriptions"
    values = {"id_inscriptions": id_inscriptions}
    results = await database.fetch_all(query, values)
    return results


async def get_active_inscriptions_by_student(id_students: str):
    query = """
        SELECT id_inscriptions
        FROM inscriptions
        WHERE id_students = :id_students
    """
    values = {"id_students": id_students}
    inscriptions = await database.fetch_all(query, values)

    active_inscriptions = []
    for inscription in inscriptions:
        inscription_id = inscription["id_inscriptions"]
        query = """
            SELECT COUNT(id_courses) AS active_courses
            FROM inscriptions_detail
            WHERE id_inscriptions = :id_inscriptions AND status = 1
        """
        values = {"id_inscriptions": inscription_id}
        result = await database.fetch_one(query, values)
        if result["active_courses"] > 0:
            active_inscriptions.append(inscription_id)

    return active_inscriptions


async def get_active_inscriptions_by_id(id_inscriptions: int):
    query = """
    SELECT id_inscriptions
    FROM inscriptions
    WHERE id_inscriptions = :id_inscriptions
    """

    values = {"id_inscriptions": id_inscriptions}
    inscriptions = await database.fetch_all(query, values)

    active_inscriptions = []
    for inscription in inscriptions:
        inscription_id = inscription["id_inscriptions"]
        query = """
        SELECT COUNT(id_courses) AS active_courses
        FROM inscriptions_detail
        WHERE id_inscriptions = :id_inscriptions AND status = 1
        """
        values = {"id_inscriptions": inscription_id}
        result = await database.fetch_one(query, values)
        if result["active_courses"] > 0:
            active_inscriptions.append(inscription_id)

    return active_inscriptions


async def get_inscription_by_student(id_students: str):
    query = f"SELECT * FROM inscriptions WHERE id_students = :id_students"
    values = {"id_students": id_students}
    results = await database.fetch_all(query, values)
    return results


async def get_all_inscriptions(response: Response):
    """
    This endpoint allows you to get all inscriptions in the database.
    """
    query = master_query
    results = await database.fetch_all(query)

    if len(results) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"No inscriptions found"
    return {"message": "All inscriptions", "data": results}


async def get_inscription(id_inscription: int, response: Response):
    """
    This endpoint allows you to get a inscription by id.

    - **id**: id of the inscription (mandatory)
    """
    results = await get_inscription_by_id(id_inscription)
    print(results)

    if len(results) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"Inscription with id: {id_inscription} not found"
    else:
        query = master_query + f" WHERE inscriptions.id_inscriptions = {id_inscription}"
        results = await database.fetch_all(query)
        response.status_code = status.HTTP_200_OK
        return {"message": "Inscription found", "data": results}


async def get_inscription_by_id_student(id_students: str, response: Response):
    """
    This endpoint allows you to get a inscription by id.

    - **id student**: id of the student (mandatory)
    """

    results = await get_inscription_by_student(id_students)
    query = master_query

    if len(results) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"Student with id: {id_students} not found"
    for result in results:
        query += f" WHERE inscriptions.id_students = '{result['id_students']}'"
        results = await database.fetch_all(query)
        response.status_code = status.HTTP_200_OK
        return {"message": "Inscription found", "data": results}


async def create_inscription(
    inscription: Inscription,
    inscriptions_detail: List[InscriptionDetail],
    response: Response,
):
    """
    This endpoint allows you to create a new inscription in the database.

    - **id**: id of the inscription (mandatory)
    - **id_students**: id of the student (mandatory)
    - **observation**: observation of the inscription (mandatory)
    - **date_inscription**: date of the inscription (mandatory)
    - **discount_family**: discount of the inscription (mandatory)
    - **inscriptions_detail**: list of inscription details (optional, can be empty)
    - **id_courses**: id of the course (mandatory for each inscription detail)
    - **unit_price**: unit price of the inscription (mandatory for each inscription detail)
    """
    students = await get_student_by_id(inscription.id_students)

    if len(students) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"Student with id: {inscription.id_students} not found"

    if students[0]["status"] == 0:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return f"Student with id: {inscription.id_students} is not active"

    for detail in inscriptions_detail:
        course = await get_courses_by_id(detail.id_courses)
        if detail.unit_price <= 0:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return "Unit price must be greater than 0"
        if len(course) == 0:
            response.status_code = status.HTTP_404_NOT_FOUND
            return f"Course with id: {detail.id_courses} not found"

    query = f"INSERT INTO inscriptions (id_students, observation, date_inscription, discount_family) VALUES (:id_students, :observation, :date_inscription, :discount_family)"
    values = {
        "id_students": inscription.id_students,
        "observation": inscription.observation,
        "date_inscription": datetime.now().strftime("%Y-%m-%d"),
        "discount_family": 0,
    }

    id_inscriptions = await database.execute(query, values)

    query = f"INSERT INTO inscriptions_detail (id_inscriptions, id_courses, unit_price, aply_discount, status) VALUES (:id_inscriptions, :id_courses, :unit_price, :aply_discount, :status)"
    for detail in inscriptions_detail:
        values = {
            "id_inscriptions": id_inscriptions,
            "id_courses": detail.id_courses,
            "unit_price": detail.unit_price,
            "aply_discount": 0,
            "status": 1,
        }
        await database.execute(query, values)

    response.status_code = status.HTTP_201_CREATED
    return {"message": "Inscription created successfully"}


async def update_inscription(update: UpdateInscription, response: Response):
    """
    This endpoint allows you to update the information of a inscription in the database.

    **id**: id of the inscription (mandatory)
    **id_course**: id of the course (mandatory)
    **status**: status of the inscription (mandatory)
    """
    inscription = await get_inscription_by_id(update.id_inscriptions)
    if len(inscription) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"Inscription with id: {update.id_inscriptions} not found"

    is_course_related = await check_course_in_inscription(
        update.id_inscriptions, update.id_courses
    )

    if not is_course_related:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return f"The course with id: {update.id_courses} is not related to the inscription with id: {update.id_inscriptions}"

    query = (
        "UPDATE inscriptions_detail "
        "SET status = :status "
        "WHERE id_inscriptions = :id_inscriptions AND id_courses = :id_courses"
    )

    values = {
        "status": update.status,
        "id_inscriptions": update.id_inscriptions,
        "id_courses": update.id_courses,
    }

    await database.execute(query, values)
    response.status_code = status.HTTP_200_OK
    return {"message": "Inscription updated successfully"}


async def delete_inscription(id_inscriptions: int, response: Response):
    """
    This endpoint allows you to delete a inscription by id.

    - **id**: id of the inscription (mandatory)
    """
    inscription = await get_inscription_by_id(id_inscriptions)

    if len(inscription) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"Inscription with id: {id_inscriptions} not found"

    is_active_inscription = await get_active_inscriptions_by_id(id_inscriptions)

    if len(is_active_inscription) > 0:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return f"Inscription with id: {id_inscriptions} has active courses"

    query = f"DELETE FROM inscriptions_detail WHERE id_inscriptions = :id_inscriptions"
    values = {"id_inscriptions": id_inscriptions}
    await database.execute(query, values)

    query = f"DELETE FROM inscriptions WHERE id_inscriptions = :id_inscriptions"
    await database.execute(query, values)

    response.status_code = status.HTTP_200_OK
    return {"message": "Inscription deleted successfully"}

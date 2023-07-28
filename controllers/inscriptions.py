from typing import List
from controllers.bills_and_set_discounts import set_discounts
from data.connection import database as database
from fastapi import status, Response
from datetime import datetime
from controllers.courses import get_courses_by_id
from controllers.students import get_student_by_id
from data.Models import Inscription, InscriptionDetail, UpdateInscription
from controllers.auxiliar_functions import (
    check_course_in_inscription,
    get_active_inscriptions_by_student,
    get_active_inscriptions_by_id,
    get_active_inscriptions_by_id_grouped_by_pack,
)
from data.queries import master_query
import json


async def get_inscription_by_id(id_inscriptions: int):
    """
    The function `get_inscription_by_id` retrieves all rows from the `inscriptions` table where the
    `id_inscriptions` column matches the provided `id_inscriptions` parameter.

    :param id_inscriptions: The parameter `id_inscriptions` is an integer that represents the ID of the
    inscription you want to retrieve from the database
    :type id_inscriptions: int
    :return: the results of a database query for inscriptions with a specific ID.
    """
    query = f"SELECT * FROM inscriptions WHERE id_inscriptions = :id_inscriptions"
    values = {"id_inscriptions": id_inscriptions}
    results = await database.fetch_all(query, values)
    return results


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


async def get_inscription_by_student(id_students: str):
    """
    The function retrieves all inscriptions associated with a specific student ID.

    :param id_students: The parameter `id_students` is a string that represents the ID of a student
    :type id_students: str
    :return: the results of a database query for inscriptions that match the given student ID.
    """
    query = f"SELECT * FROM inscriptions WHERE id_students = :id_students"
    values = {"id_students": id_students}
    results = await database.fetch_all(query, values)
    return results


async def get_inscription(id_inscription: int, response: Response):
    """
    This endpoint allows you to get a inscription by id.

    - **id**: id of the inscription (mandatory)
    """
    results = await get_inscription_by_id(id_inscription)

    if len(results) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"Inscription with id: {id_inscription} not found"
    else:
        query = master_query + f" WHERE inscriptions.id_inscriptions = {id_inscription}"
        results = await database.fetch_all(query)
        response.status_code = status.HTTP_200_OK
        return {"message": "Inscription found", "data": results}


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


async def create_inscription(
    inscription: Inscription,
    inscriptions_detail: List[InscriptionDetail],
    response: Response,
):
    """
    This endpoint allows you to create a new inscription in the database.

    - **id_students**: id of the student (mandatory)
    - **observation**: observation of the inscription (optional, can be empty)
    - **id_courses**: id of the course (mandatory for each inscription detail)
    """

    # Validate student in different ways
    if inscription.id_students == "string" or inscription.id_students == "":
        return "Student id is mandatory"

    students = await get_student_by_id(inscription.id_students)

    if len(students) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"Student with id: {inscription.id_students} not found"

    if students[0]["status"] == 0:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return f"Student with id: {inscription.id_students} is not active"

    # Iterate over inscription details and create courses
    for detail in inscriptions_detail:
        query_check_existing = """
            SELECT inscriptions_detail.id_courses
            FROM inscriptions_detail
            JOIN inscriptions ON inscriptions.id_inscriptions = inscriptions_detail.id_inscriptions
            WHERE inscriptions.id_students = :id_students AND inscriptions_detail.id_courses = :id_courses
        """

        existing_inscription = await database.fetch_one(
            query_check_existing,
            values={
                "id_students": inscription.id_students,
                "id_courses": detail.id_courses,
            },
        )

        # Validate if the student is already enrolled in the course
        if existing_inscription:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return f"Student with id: {inscription.id_students} is already enrolled in the course with id: {detail.id_courses}"

        course = await get_courses_by_id(detail.id_courses)

        # Validate if the course exists
        if len(course) == 0:
            response.status_code = status.HTTP_404_NOT_FOUND
            return f"Course with id: {detail.id_courses} not found"

    query = f"INSERT INTO inscriptions (id_students, observation, date_inscription, discount_family) VALUES (:id_students, :observation, :date_inscription, :discount_family)"

    if inscription.observation == "" or inscription.observation == "string":
        inscription.observation = "Sin observaciones"

    # Define values and discount for each inscription
    aply_discount = 0
    values = {
        "id_students": inscription.id_students,
        "observation": inscription.observation,
        "date_inscription": datetime.now().strftime("%Y-%m-%d"),
        "discount_family": aply_discount,
    }

    id_inscriptions = await database.execute(query, values)

    query = f"INSERT INTO inscriptions_detail (id_inscriptions, id_courses, unit_price, aply_discount, status) VALUES (:id_inscriptions, :id_courses, :unit_price, :aply_discount, :status)"
    for detail in inscriptions_detail:
        current_course = await get_courses_by_id(detail.id_courses)
        unit_price = current_course[0]["prices"]
        values = {
            "id_inscriptions": id_inscriptions,
            "id_courses": detail.id_courses,
            "unit_price": unit_price,
            "aply_discount": 0,
            "status": 1,
        }
        await database.execute(query, values)

    # Validate if the student has a familiar
    familiar_students = students[0]["id_familiar"]
    familiar = students[0]["familiar"]

    # Iterate over familiar students to search for active inscriptions and apply discount
    if len(familiar_students) > 1:
        familiar_students = json.loads(familiar_students)
        for student in familiar_students:
            familiar_is_active = await get_active_inscriptions_by_student(student)
            if len(familiar_is_active) >= 1:
                aply_discount = 0.1
                query_discount = f"UPDATE inscriptions SET discount_family = :discount_family WHERE id_students = :id_students"

                values = {
                    "discount_family": aply_discount,
                    "id_students": familiar,
                }

                await database.execute(query_discount, values)

    if len(familiar_students) == 1:
        familiar_is_active = await get_active_inscriptions_by_student(familiar)
        if len(familiar_is_active) >= 1:
            aply_discount = 0.1
            query_discount = f"UPDATE inscriptions SET discount_family = :discount_family WHERE id_students = :id_students"

            values = {
                "discount_family": aply_discount,
                "id_students": familiar,
            }

            await database.execute(query_discount, values)

    # Get active packs and set discounts
    active_packs = await get_active_inscriptions_by_id_grouped_by_pack(
        inscription.id_students
    )

    # Set discounts with the active packs
    await set_discounts(active_packs)
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

    # Validate a student, and extract the familiar
    student = await get_student_by_id(inscription[0]["id_students"])
    id_student = student[0]["id_students"]
    familiar = student[0]["familiar"]
    familiar_to_update = student[0]["familiar"]

    # Validate if the course is related to the inscription
    is_course_related = await check_course_in_inscription(
        update.id_inscriptions, update.id_courses
    )

    if not is_course_related:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return f"The course with id: {update.id_courses} is not related to the inscription with id: {update.id_inscriptions}"

    # Update inscription detail in database
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

    # Get all active inscriptions for the student and familiars
    is_active_inscription = await get_active_inscriptions_by_student(id_student)
    get_familiar = await get_student_by_id(familiar)

    if len(get_familiar) != 0:
        familiar_list = json.loads(get_familiar[0]["id_familiar"])
        aply_discount = 0

        if len(is_active_inscription) == 0 and id_student in familiar_list:
            familiar_list.remove(id_student)

        if len(is_active_inscription) > 0 and id_student not in familiar_list:
            familiar_list.append(id_student)

        for familiar in familiar_list:
            familiar_is_active = await get_active_inscriptions_by_student(familiar)

            if len(familiar_is_active) >= 1:
                aply_discount = 0.1

        updated_familiar_list = json.dumps(familiar_list)
        query = f"UPDATE students SET id_familiar = :id_familiar WHERE id_students = :id_students"

        values = {
            "id_familiar": updated_familiar_list,
            "id_students": familiar,
        }

        await database.execute(query, values)

        query_discount = f"UPDATE inscriptions SET discount_family = :discount_family WHERE id_students = :id_students"
        values = {
            "discount_family": aply_discount,
            "id_students": familiar_to_update,
        }

        # Update inscription in database, and set discounts based on active packs
        await database.execute(query_discount, values)
        active_packs = await get_active_inscriptions_by_id_grouped_by_pack(id_student)
        await set_discounts(active_packs)
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

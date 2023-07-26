from typing import List, Dict
from controllers.courses import get_courses_by_id
from controllers.students import get_student_by_id
from data.Models import Inscription, InscriptionDetail, UpdateInscription
from data.connection import database as database
from fastapi import status, Response
from datetime import datetime
import json


master_query = "SELECT inscriptions.id_inscriptions AS id_inscriptions,inscriptions.date_inscription AS date_inscription,students.id_students AS id_student,students.first_name AS first_name,students.last_name AS last_name,students.phone AS phone,courses.id_courses AS id_courses,classes.name AS class_name,levels.name AS level_name,professors.first_name AS professor_first_name,professors.last_name AS professor_last_name,classes.id_packs AS packs,inscriptions_detail.unit_price AS unit_price,inscriptions_detail.aply_discount AS aply_discount,inscriptions.discount_family AS discount_family,inscriptions_detail.status AS status,inscriptions.observation AS observation FROM inscriptions INNER JOIN students ON inscriptions.id_students = students.id_students INNER JOIN inscriptions_detail ON inscriptions.id_inscriptions = inscriptions_detail.id_inscriptions INNER JOIN courses ON inscriptions_detail.id_courses = courses.id_courses INNER JOIN classes ON courses.id_classes = classes.id_classes INNER JOIN levels ON courses.id_levels = levels.id_levels INNER JOIN professors ON courses.id_professors = professors.id_professors"

query_status = "SELECT inscriptions_detail.status AS status FROM inscriptions INNER JOIN students ON inscriptions.id_students=students.id_students INNER JOIN inscriptions_detail ON inscriptions.id_inscriptions=inscriptions_detail.id_inscriptions INNER JOIN courses ON inscriptions_detail.id_courses=courses.id_courses INNER JOIN classes ON courses.id_classes=classes.id_classes INNER JOIN levels ON courses.id_levels=levels.id_levels INNER JOIN professors ON courses.id_professors=professors.id_professors WHERE students.id_students= :id_students AND inscriptions_detail.status=1"


async def check_status_in_inscription_by_id_student(id_students: str):
    query = query_status
    values = {"id_students": id_students}
    results = await database.fetch_all(query, values)

    if len(results) == 0:
        return False
    else:
        return True


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


async def get_active_inscriptions_by_id_grouped_by_pack(
    id_students: str,
) -> Dict[int, Dict[int, int]]:
    query = """
        SELECT inscriptions_detail.id_inscriptions AS id_inscriptions, inscriptions_detail.id_courses AS id_courses, classes.id_packs AS packs, inscriptions_detail.status AS status
        FROM inscriptions
        INNER JOIN students ON inscriptions.id_students = students.id_students
        INNER JOIN inscriptions_detail ON inscriptions.id_inscriptions = inscriptions_detail.id_inscriptions
        INNER JOIN courses ON inscriptions_detail.id_courses = courses.id_courses
        INNER JOIN classes ON courses.id_classes = classes.id_classes
        INNER JOIN levels ON courses.id_levels = levels.id_levels
        INNER JOIN professors ON courses.id_professors = professors.id_professors
        WHERE students.id_students = :id_students AND inscriptions_detail.status = 1
    """

    results = await database.fetch_all(query, values={"id_students": id_students})
    active_inscriptions_by_pack = {}

    for result in results:
        pack_id = result["packs"]
        insc_id = result["id_inscriptions"]
        course_id = result["id_courses"]

        if pack_id not in active_inscriptions_by_pack:
            active_inscriptions_by_pack[pack_id] = {}

        active_inscriptions_by_pack[pack_id][insc_id] = course_id

    return active_inscriptions_by_pack


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

    - **id_students**: id of the student (mandatory)
    - **observation**: observation of the inscription (optional, can be empty)
    - **id_courses**: id of the course (mandatory for each inscription detail)
    """
    if inscription.id_students == "string" or inscription.id_students == "":
        return "Student id is mandatory"

    students = await get_student_by_id(inscription.id_students)

    if len(students) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"Student with id: {inscription.id_students} not found"

    familiar_students = students[0]["id_familiar"]

    aply_discount = 0

    if len(familiar_students) > 1:
        familiar_students = json.loads(familiar_students)
        for student in familiar_students:
            familiar_is_active = await get_active_inscriptions_by_student(student)
            if len(familiar_is_active) >= 1:
                aply_discount = 0.1

    if students[0]["status"] == 0:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return f"Student with id: {inscription.id_students} is not active"

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

        if existing_inscription:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return f"Student with id: {inscription.id_students} is already enrolled in the course with id: {detail.id_courses}"

        course = await get_courses_by_id(detail.id_courses)
        if len(course) == 0:
            response.status_code = status.HTTP_404_NOT_FOUND
            return f"Course with id: {detail.id_courses} not found"

    query = f"INSERT INTO inscriptions (id_students, observation, date_inscription, discount_family) VALUES (:id_students, :observation, :date_inscription, :discount_family)"

    if inscription.observation == "" or inscription.observation == "string":
        inscription.observation = "Sin observaciones"

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

    active_packs = await get_active_inscriptions_by_id_grouped_by_pack(
        inscription.id_students
    )

    print(active_packs)
    print(type(active_packs))
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


async def get_payments_by_student(id_students: str, response: Response):
    student = await get_inscription_by_id_student(id_students, response)

    if student == f"Student with id: {id_students} not found":
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": f"Student with id: {id_students} not have inscriptions"}

    student = student["data"]
    student_name = f"{student[0][3]} {student[0][4]}"
    total = 0
    result_data = {"student_name": student_name, "courses": []}

    for result in student:
        class_name = result[7]
        level_name = result[8]
        pack_number = result[11]
        unit_price = result[12]
        aply_discount = float(result[13])
        discount_family = float(result[14])
        status = result[15]

        course_data = {
            "class_name": class_name,
            "level_name": level_name,
            "pack_number": pack_number,
            "unit_price": unit_price,
        }

        if aply_discount == 0:
            course_data["discount"] = "No tiene aplicado ningun descuento"
        elif aply_discount == 0.5:
            course_data["discount"] = "Se le aplicó un descuento del 50%"
        elif aply_discount == 0.75:
            course_data["discount"] = "Se le aplicó un descuento del 75%"

        if aply_discount != 0:
            course_data["final_price"] = unit_price - (unit_price * aply_discount)

        if status != 0:
            total += unit_price - (unit_price * aply_discount)
            result_data["courses"].append(course_data)

    if discount_family == 0:
        result_data["family_discount"] = "No tiene descuento familiar"
        result_data["total_to_pay"] = total
    elif discount_family == 0.1:
        result_data[
            "family_discount"
        ] = "Se le aplicó un descuento del 10% por tener un familiar"
        result_data["total_to_pay"] = total - (total * 0.1)

    return result_data

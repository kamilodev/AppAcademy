from typing import Dict
from data.queries import query_status
from data.connection import database as database


async def check_status_in_inscription_by_id_student(id_students: str):
    """
    The function checks the status of an inscription by the ID of a student.

    :param id_students: The parameter `id_students` is a string that represents the ID of a student
    :type id_students: str
    :return: a boolean value. If the length of the results is 0, it returns False. Otherwise, it returns
    True.
    """
    query = query_status
    values = {"id_students": id_students}
    results = await database.fetch_all(query, values)

    return results


async def check_course_in_inscription(id_inscription: int, id_course: int) -> bool:
    """
    The function `check_course_in_inscription` checks if a course is present in an inscription.

    :param id_inscription: The id of the inscription you want to check
    :type id_inscription: int
    :param id_course: The `id_course` parameter is an integer that represents the ID of a course
    :type id_course: int
    :return: a boolean value. It returns True if there is a matching record in the "inscriptions_detail"
    table with the given "id_inscription" and "id_course" values. It returns False if there is no
    matching record.
    """
    query = "SELECT id_inscriptions FROM inscriptions_detail WHERE id_inscriptions = :id_inscription AND id_courses = :id_course"
    values = {"id_inscription": id_inscription, "id_course": id_course}
    result = await database.fetch_all(query, values)
    return len(result) > 0


async def get_active_inscriptions_by_student(id_students: str):
    """
    The function `get_active_inscriptions_by_student` retrieves a list of active inscriptions for a
    given student ID.

    :param id_students: The parameter `id_students` is a string that represents the ID of a student
    :type id_students: str
    :return: a list of active inscriptions for a given student.
    """
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
    """
    The function `get_active_inscriptions_by_id` retrieves a list of active inscriptions based on the
    provided `id_inscriptions`.

    :param id_inscriptions: The parameter "id_inscriptions" is an integer that represents the ID of the
    inscriptions you want to retrieve
    :type id_inscriptions: int
    :return: a list of active inscriptions.
    """
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

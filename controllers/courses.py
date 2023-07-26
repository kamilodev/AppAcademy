from data.connection import database as database
from fastapi import status, Response
from data.Models import NewCourses


master_query = "SELECT c.id_courses,cl.name AS classes_name,l.name AS levels_name,p.first_name AS professor_name,p.last_name AS professor_surname,c.max_students,c.prices,cl.id_packs AS packs FROM courses c JOIN classes cl ON c.id_classes=cl.id_classes JOIN levels l ON c.id_levels=l.id_levels JOIN professors p ON c.id_professors=p.id_professors"


async def get_courses_by_id(id_courses: int):
    query = f"SELECT * FROM courses WHERE id_courses = {id_courses}"
    results = await database.fetch_all(query)
    return results


async def get_courses(id_courses: int, response: Response):
    """
    This endpoint allows you to get a courses by id.

    - **id**: id of the course (mandatory)
    """
    query = f"{master_query} WHERE c.id_courses = {id_courses}"
    results = await get_courses_by_id(id_courses)

    if len(results) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"Course with id: {id_courses} not found"
    else:
        response.status_code = status.HTTP_200_OK
        results = await database.fetch_all(query)
        return {"message": "Course found", "data": results[0]}


async def get_all_courses(response: Response):
    """
    This endpoint allows you to get all courses in the database.
    """
    query = f"{master_query} ORDER BY c.id_courses;"
    results = await database.fetch_all(query)

    if len(results) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"No courses found"
    return {"message": "All courses", "data": results}


async def get_all_courses_by_professor(name_professor: str, response: Response):
    """
    This endpoint allows you to get all courses in the database by name professor.
    """
    query = (
        f"{master_query} WHERE p.first_name = '{name_professor}' ORDER BY c.id_courses;"
    )
    if len(await database.fetch_all(query)) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"Professor with name: {name_professor} not found"

    results = await database.fetch_all(query)
    print(len(results))
    return {"message": "All courses", "data": results}


async def get_course_by_name(name_course: str, response: Response):
    """
    This endpoint allows you to get a course by name.
    """
    query = f"{master_query} WHERE cl.name = '{name_course}' ORDER BY c.id_courses;"
    if len(await database.fetch_all(query)) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"Course with name: {name_course} not found"

    results = await database.fetch_all(query)
    print(len(results))
    return {"message": "All courses", "data": results}


async def get_courses_by_level(level: str, response: Response):
    """
    The function `get_courses_by_level` retrieves courses based on a specified level and returns the
    results.

    :param level: The `level` parameter is a string that represents the level of the course. It is used
    to filter the courses based on their level
    :type level: str
    :param response: The `response` parameter is an instance of the `Response` class. It is used to set
    the status code of the HTTP response. In this case, if the course with the specified level is not
    found, the status code is set to 404 (Not Found)
    :type response: Response
    :return: a dictionary with two keys: "message" and "data". The value of the "message" key is the
    string "All courses", and the value of the "data" key is the results of the query, which is a list
    of courses that match the specified level.
    """
    """
    This endpoint allows you to get a course by level.
    """
    query = f"{master_query} WHERE l.name = '{level}' ORDER BY c.id_courses;"
    if len(await database.fetch_all(query)) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"Course with level: {level} not found"

    results = await database.fetch_all(query)
    return {"message": "All courses", "data": results}


async def create_course(course: NewCourses, response: Response):
    """
    This endpoint allows you to create a new course in the database.

    - **id**: id of the course (mandatory)
    - **name_class**: name of the class (mandatory)
    - **level**: level of the class (mandatory)
    - **name_professor**: name of the professor (mandatory)
    - **max_students**: max students of the course (mandatory)
    - **prices**: price of the course (mandatory)
    """
    query_class = f"SELECT * FROM classes WHERE name = '{course.name_class}'"
    query_level = f"SELECT * FROM levels WHERE name = '{course.level}'"
    query_professor = (
        f"SELECT * FROM professors WHERE first_name = '{course.name_professor}'"
    )

    class_results = await database.fetch_all(query_class)
    level_results = await database.fetch_all(query_level)
    professor_results = await database.fetch_all(query_professor)

    if len(class_results) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"Class with name: {course.name_class} not found"
    elif len(level_results) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"Level with name: {course.level} not found"
    elif len(professor_results) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"Professor with name: {course.name_professor} not found"

    class_id = class_results[0]["id_classes"]
    level_id = level_results[0]["id_levels"]
    professor_id = professor_results[0]["id_professors"]

    query_duplicate = (
        f"SELECT * FROM courses "
        f"WHERE id_classes = {class_id} "
        f"AND id_levels = {level_id} "
        f"AND id_professors = {professor_id}"
    )
    duplicate_results = await database.fetch_all(query_duplicate)

    if len(duplicate_results) > 0:
        response.status_code = status.HTTP_409_CONFLICT
        return "A course with the same professor, level, or class already exists"

    query = (
        "INSERT INTO courses (id_courses, id_classes, id_levels, id_professors, "
        "max_students, prices) "
        "VALUES (:id_courses, :id_classes, :id_levels, :id_professors, "
        ":max_students, :prices)"
    )
    values = {
        "id_courses": course.id_courses,
        "id_classes": class_id,
        "id_levels": level_id,
        "id_professors": professor_id,
        "max_students": course.max_students,
        "prices": course.prices,
    }

    results = await database.execute(query, values)
    return {"message": "Course created successfully", "data": results}


async def update_course(course: NewCourses, response: Response):
    """
    This endpoint allows you to update a course in the database.

    - **id_courses**: id of the course (mandatory)
    - **classes_name**: name of the class (optional)
    - **levels_name**: level of the class (optional)
    - **professor_name**: name of the professor (optional)
    - **professor_surname**: surname of the professor (optional)
    - **max_students**: max students of the course (optional)
    - **prices**: price of the course (optional)
    """
    query = f"{master_query} WHERE c.id_courses = {course.id_courses}"
    results = await database.fetch_all(query)

    if len(results) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"Course with id: {course.id_courses} not found"

    update_fields = {}
    if course.name_class == "string":
        update_fields["id_classes"] = results[0]["classes_name"]
    else:
        update_fields["id_classes"] = course.name_class
    if course.level == "string":
        update_fields["id_levels"] = results[0]["levels_name"]
    else:
        update_fields["id_levels"] = course.level
    if course.name_professor == "string":
        update_fields["id_professors"] = results[0]["professor_name"]
    else:
        update_fields["id_professors"] = course.name_professor
    if course.max_students == 0:
        update_fields["max_students"] = results[0]["max_students"]
    else:
        update_fields["max_students"] = course.max_students
    if course.prices == 0:
        update_fields["prices"] = results[0]["prices"]
    else:
        update_fields["prices"] = course.prices

    if (
        update_fields["id_classes"] == results[0]["classes_name"]
        and update_fields["id_levels"] == results[0]["levels_name"]
        and update_fields["id_professors"] == results[0]["professor_name"]
        and update_fields["max_students"] == results[0]["max_students"]
        and update_fields["prices"] == results[0]["prices"]
    ):
        response.status_code = status.HTTP_304_NOT_MODIFIED
        return {"message": "Nothing to update"}

    query_class = f"SELECT * FROM classes WHERE name = '{update_fields['id_classes']}'"
    query_level = f"SELECT * FROM levels WHERE name = '{update_fields['id_levels']}'"
    query_professor = f"SELECT * FROM professors WHERE first_name = '{update_fields['id_professors']}'"

    class_results = await database.fetch_all(query_class)
    level_results = await database.fetch_all(query_level)
    professor_results = await database.fetch_all(query_professor)

    if len(class_results) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"Class with name: {update_fields['id_classes']} not found"
    if len(level_results) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"Level with name: {update_fields['id_levels']} not found"
    if len(professor_results) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"Professor with name: {update_fields['id_professors']} not found"

    class_id = class_results[0]["id_classes"]
    level_id = level_results[0]["id_levels"]
    professor_id = professor_results[0]["id_professors"]

    if (
        update_fields["max_students"] == results[0]["max_students"]
        and update_fields["prices"] == results[0]["prices"]
    ):
        query_duplicate = (
            f"SELECT * FROM courses "
            f"WHERE id_classes = {class_id} "
            f"AND id_levels = {level_id} "
            f"AND id_professors = {professor_id}"
        )
        duplicate_results = await database.fetch_all(query_duplicate)

        if len(duplicate_results) > 0:
            response.status_code = status.HTTP_409_CONFLICT
            return "A course with the same professor, level, or class already exists"

    query = (
        "UPDATE courses SET "
        "id_classes = :id_classes, "
        "id_levels = :id_levels, "
        "id_professors = :id_professors, "
        "max_students = :max_students, "
        "prices = :prices "
        "WHERE id_courses = :id_courses"
    )

    values = {
        "id_courses": course.id_courses,
        "id_classes": class_id,
        "id_levels": level_id,
        "id_professors": professor_id,
        "max_students": update_fields["max_students"],
        "prices": update_fields["prices"],
    }

    response.status_code = status.HTTP_200_OK
    results = await database.execute(query, values)
    return {"message": "Course updated successfully"}


# TODO: Validar que no existan inscripciones
async def delete_course(id_courses: int, response: Response):
    """
    This endpoint allows you to delete a course in the database.

    **id_courses**: id of the course (mandatory)
    """

    results = await get_courses_by_id(id_courses)

    if len(results) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"Course with id: {id_courses} not found"

    delete_query = f"DELETE FROM courses WHERE id_courses = {id_courses}"
    await database.execute(delete_query)
    return f"Course with id: {id_courses} deleted"

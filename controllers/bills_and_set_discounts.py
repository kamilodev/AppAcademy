from typing import Dict
from fastapi import status, Response
from data.connection import database as database


async def get_payments_by_student(id_students: str, response: Response):
    """
    The function `get_payments_by_student` retrieves payment information for a student based on their
    ID.

    :param id_students: The `id_students` parameter is a string that represents the ID of the student
    for whom we want to retrieve the payments. This ID is used to fetch the student's information from
    the database
    :type id_students: str
    :param response: The `response` parameter is an instance of the `Response` class, which is typically
    used to send HTTP responses. It allows you to set the status code and return data in the response
    body
    :type response: Response
    :return: a dictionary named `result_data` which contains the following keys:
    """
    from controllers.inscriptions import get_inscription_by_id_student

    student = await get_inscription_by_id_student(id_students, response)
    if student == f"Student with id: {id_students} not found":
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": f"Student with id: {id_students} not have inscriptions"}

    student = student["data"]
    student_name = f"{student[0]['first_name']} {student[0]['last_name']}"
    total = 0

    result_data = {"student_name": student_name, "courses": []}

    for result in student:
        class_name = result["class_name"]
        level_name = result["level_name"]
        pack_number = result["packs"]
        unit_price = result["unit_price"]
        aply_discount = float(result["aply_discount"])
        discount_family = float(result["discount_family"])
        status = result["status"]

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

        discount = "active" if discount_family != 0 else "inactive"

        if discount == "active":
            result_data[
                "family_discount"
            ] = "Se le aplicó un descuento del 10% por tener un familiar"
            result_data["total_to_pay"] = total - (total * 0.1)
        elif discount == "inactive":
            result_data["family_discount"] = "No tiene descuento familiar"
            result_data["total_to_pay"] = total

    return result_data


async def set_discounts(active_courses: Dict):
    """
    The function `set_discounts` updates the `aply_discount` field in the `inscriptions_detail` table
    based on certain conditions.

    :param active_courses: The `active_courses` parameter is a dictionary that contains information
    about the active courses. The keys of the dictionary represent the pack IDs, and the values are
    dictionaries that contain the inscriptions and course IDs for each pack
    :type active_courses: Dict
    """
    for pack_id in active_courses:
        if pack_id == 1 or pack_id == 2:
            pack = active_courses[pack_id].copy()

            num_courses = len(pack)
            for index, (insc_id, course_id) in enumerate(pack.items(), 1):
                if index == 2:
                    query = f"UPDATE inscriptions_detail SET aply_discount = 0.5 WHERE id_inscriptions = :id_inscriptions AND id_courses = :id_courses"
                elif num_courses > 2 and index >= 3:
                    query = f"UPDATE inscriptions_detail SET aply_discount = 0.75 WHERE id_inscriptions = :id_inscriptions AND id_courses = :id_courses"
                else:
                    query = f"UPDATE inscriptions_detail SET aply_discount = 0 WHERE id_inscriptions = :id_inscriptions AND id_courses = :id_courses"

                values = {
                    "id_inscriptions": insc_id,
                    "id_courses": course_id,
                }
                await database.execute(query, values)

        else:
            for insc_id, course_id in active_courses[pack_id].items():
                query = f"UPDATE inscriptions_detail SET aply_discount = 0 WHERE id_inscriptions = :id_inscriptions AND id_courses = :id_courses"
                values = {
                    "id_inscriptions": insc_id,
                    "id_courses": course_id,
                }
                await database.execute(query, values)

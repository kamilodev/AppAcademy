from data.connection import database as database
from fastapi import status, Response
from data.Models import DeleteProfessor, Professor


async def get_professor_by_id(id_professors: str):
    query = f"SELECT * FROM professors WHERE id_professors = :id_professors"
    values = {"id_professors": id_professors}
    results = await database.fetch_all(query, values)
    return results


async def get_professor(id_professors: str, response: Response):
    """
    This endpoint allows you to get a professor by id.

    - **id**: DNI of the professor (mandatory)
    """
    results = await get_professor_by_id(id_professors)

    if len(results) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"Professor with id: {id_professors} not found"
    else:
        response.status_code = status.HTTP_200_OK
        return {"message": "Professor found", "data": results[0]}
    

async def get_all_professors():
    """
    This endpoint allows you to get all professors in the database.
    """
    query = "SELECT * FROM professors ORDER BY id_professors ASC"
    results = await database.fetch_all(query)
    return {"message": "All professors", "data": results}


async def create_professor(professor: Professor, response: Response):
    """
    This endpoint allows you to create a new professor in the database.

    - **id**: DNI of the professor (mandatory)
    - **first_name**: First name of the professor (mandatory)
    - **last_name**: Last name of the professor (mandatory)
    - **phone**: Phone number of the professor (mandatory)
    - **email**: Email of the professor (mandatory)
    """

    default_values = ["string", "", 0]

    for field in professor.__fields__:
        if professor.__getattribute__(field) in default_values:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return f"Field {field} cannot be empty"
        
    query = f"INSERT INTO professors (id_professors, first_name, last_name, phone, email) VALUES (:id_professors, :first_name, :last_name, :phone, :email)"
    values = {
        "id_professors": professor.id_professors,
        "first_name": professor.first_name,
        "last_name": professor.last_name,
        "phone": professor.phone,
        "email": professor.email,
    }
    duplicate_professor = await get_professor_by_id(professor.id_professors)
    if len(duplicate_professor) > 0:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return f"Professor with id: {professor.id_professors} already exists"
    
    await database.execute(query=query, values=values)

    return {"message": "Professor created successfully"}


async def update_professor(professor: Professor, response: Response):
    """
    This endpoint allows you to update the information of a professor in the database.

    - **id**: DNI of the professor (mandatory)
    - **first_name**: First name of the professor (mandatory)
    - **last_name**: Last name of the professor (mandatory)
    - **phone**: Phone number of the professor (mandatory)
    - **email**: Email of the professor (mandatory)

    """
    results = await get_professor_by_id(professor.id_professors)

    if professor.id_professors == "" or professor.id_professors == "string":
        response.status_code = status.HTTP_400_BAD_REQUEST
        return f"Professor id cannot be empty"

    if len(results) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"Professor with id: {professor.id_professors} not found"

    update_fields = {}

    default_values = ["string", 0]

    for field in professor.__fields__:
        if field == "id_professors":
            continue
        if professor.__getattribute__(field) in default_values:
            continue

        update_fields[field] = professor.__getattribute__(field)

    if len(update_fields) == 0:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return f"No fields to update for professor with id: {professor.id_professors}"

    set_query = ", ".join(f"{field} = :{field}" for field in update_fields)
    values = {"id_professors": professor.id_professors, **update_fields}

    query = f"UPDATE professors SET {set_query} WHERE id_professors = :id_professors"
    await database.execute(query=query, values=values)

    return f"Professor with id {professor.id_professors} updated successfully"


async def delete_professor(professor: DeleteProfessor, response: Response):
    """
    This endpoint allows you to delete a professor by id.

    - **id**: DNI of the professor (mandatory)
    """
    results = await get_professor_by_id(professor.id_professors)

    if professor.id_professors == "" or professor.id_professors == "string":
        response.status_code = status.HTTP_400_BAD_REQUEST
        return f"Professor id cannot be empty"

    if len(results) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"Professor with id: {professor.id_professors} not found"

    delete_query = f"DELETE FROM professors WHERE id_professors = :id_professors"
    values = {"id_professors": professor.id_professors}

    await database.execute(delete_query, values)
    response.status_code = status.HTTP_200_OK
    return f"Professor with id {professor.id_professors} deleted"
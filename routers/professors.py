from fastapi import APIRouter, Response, status
from Models import Professor
from connection import database as database

router = APIRouter(prefix="/professors", tags=["Professors"])


@router.post("/", summary="Create a new professor")
async def create_professors(professor: Professor):
    """
    This endpoint allows you to create a new professor in the database.

    - **id**: DNI of the professor (mandatory)
    - **first_name**: First name of the professor (mandatory)
    - **last_name**: Last name of the professor (mandatory)
    - **phone**: Phone number of the professor (mandatory)
    - **email**: Email of the professor (mandatory)
    """

    query = f"""
    INSERT INTO professors
            (
            id_professors,
            first_name,
            last_name,
            phone,
            email,
            address)
        VALUES
            (
            :id_professors,
            :first_name,
            :last_name,
            :phone,
            :email,
            :address)
        """
    values = {
        "id_professors": professor.id_professors,
        "first_name": professor.first_name,
        "last_name": professor.last_name,
        "phone": professor.phone,
        "email": professor.email,
        "address": professor.address,
    }
    await database.execute(query=query, values=values)
    print(query)
    return {"message": "Professor created successfully"}


@router.get(
    "/{id_professors}",
    status_code=status.HTTP_200_OK,
    tags=["Professors"],
    summary="Get a prof by id",
)
async def get_professors(id_professors: int, response: Response):
    """
    This endpoint allows you to get a prof by id.

    - **id**: DNI of the professor (mandatory)
    """
    query = f"SELECT * FROM professors WHERE id_professors = {id_professors}"
    results = await database.fetch_all(query)
    if len(results) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"Proffesor with id: {id_professors} not found"
    else:
        response.status_code = status.HTTP_200_OK
        return {"message": "Professor found", "data": results[0]}


@router.delete(
    "/{id_professors}",
    status_code=status.HTTP_200_OK,
    summary="Delete a professor by id",
)
async def delete_professors(id_professors: int, response: Response):
    """
    This endpoint allows you to delete a prof by id.

    - **id**: DNI of the prof (mandatory)
    """

    query = f"SELECT * FROM professors WHERE id_professors = {id_professors}"
    results = await database.fetch_all(query)
    if len(results) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"Student with id: {id_professors} not found"

    delete_query = f"DELETE FROM professors WHERE id_professors = {id_professors}"
    await database.execute(delete_query)

    response.status_code = status.HTTP_200_OK
    return {"message": "Profesor deleted"}


@router.put("/")
async def update_professors(professor: Professor):
    query = f"""
        UPDATE professors
        SET first_name = :first_name,
            last_name = :last_name,
            phone = :phone,
            email = :email,
            address = address
        WHERE id_professors = :id_professors
    """
    values = {
        "id_professors": professor.id_professors,
        "first_name": professor.first_name,
        "last_name": professor.last_name,
        "phone": professor.phone,
        "email": professor.email,
        "address": professor.address,
    }
    await database.execute(query=query, values=values)
    return {"message": "Professor updated successfully"}


@router.get(
    "/",
    summary="Get all professors",
    response_description="All professors in database shown",
)
async def all_professors():
    """
    This endpoint allows you to get all professors in the database.
    """
    query = "SELECT * FROM professors"
    results = await database.fetch_all(query)
    return {"message": "All Professors", "data": results}

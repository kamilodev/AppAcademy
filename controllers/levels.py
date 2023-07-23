from data.connection import database as database
from fastapi import status, Response
from data.Models import CreateLevel, Level


async def get_level_by_id(id_levels: int):
    query = f"SELECT * FROM levels WHERE id_levels = {id_levels}"
    results = await database.fetch_all(query)
    return results


async def get_level(id_levels: int, response: Response):
    """
    This endpoint allows you to get a level by id.

    - **id**: id of the level (mandatory)
    """
    results = await get_level_by_id(id_levels)

    if len(results) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"Level with id: {id_levels} not found"
    else:
        response.status_code = status.HTTP_200_OK
        return {"message": "Level found", "data": results[0]}


async def get_all_levels(response: Response):
    """
    This endpoint allows you to get all levels in the database.
    """
    query = "SELECT * FROM levels"
    results = await database.fetch_all(query)

    if len(results) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"No levels found"
    return {"message": "All levels", "data": results}


async def create_level(level: CreateLevel):
    """
    This endpoint allows you to create a new level in the database.

    - **name**: name of new the level
    """
    query = f"INSERT INTO levels (name) VALUES (:name)"
    values = {
        "name": level.name,
    }
    await database.execute(query=query, values=values)

    return {"message": "Level created successfully"}


# TODO: Validate if familiar exists
async def update_level(level: Level, response: Response):
    """
    This endpoint allows you to update the information of a level in the database.

    - **id**: id of the level (mandatory)
    - **name**: name of the level

    """
    results = await get_level_by_id(level.id_levels)

    if len(results) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"Level with id: {level.id_levels} not found"

    update_fields = {}

    if level.name != "string":
        update_fields["name"] = level.name

    if len(update_fields) == 0:
        return f"No fields to update for level with id: {level.id_levels}"

    set_query = ", ".join(f"{field} = :{field}" for field in update_fields)
    values = {"id_levels": level.id_levels, **update_fields}

    query = f"UPDATE levels SET {set_query} WHERE id_levels = :id_levels"
    await database.execute(query=query, values=values)

    return f"Level with id {level.id_levels} updated successfully"


async def delete_level(id_levels: int, response: Response):
    """
    This endpoint allows you to delete a level by id.

    - **id**: id of the level (mandatory)
    """
    results = await get_level_by_id(id_levels)

    if len(results) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"Level with id: {id_levels} not found"

    delete_query = f"DELETE FROM levels WHERE id_levels = {id_levels}"
    await database.execute(delete_query)

    response.status_code = status.HTTP_200_OK
    return f"Level with id {id_levels} deleted"

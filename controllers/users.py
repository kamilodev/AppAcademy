from fastapi import status, Response, Depends
from data.connection import database as database
from data.Models import User, UserUpdate, DeleteUser


async def get_user_by_id(id_users: str) -> dict:
    """
    The function `get_user_by_id` retrieves user information from a database based on the provided user
    ID.

    :param id_users: The parameter `id_users` is a string that represents the ID of the user you want to
    retrieve from the database
    :type id_users: str
    :return: the results of a database query.
    """
    query = "SELECT * FROM users WHERE id_users = :id_users"
    values = {"id_users": id_users}
    return await database.fetch_all(query, values)


async def get_user(id_users: str, response: Response) -> dict:
    """
    This endpoint allows you to get a user by id.

    - **id**: DNI of the user (mandatory)
    """
    results = await get_user_by_id(id_users)

    if not results:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"User with id: {id_users} not found"
    response.status_code = status.HTTP_200_OK
    return {"message": "User found", "data": results[0]}


async def get_user_by_name(name: str) -> dict:
    """
    This endpoint allows you to get a user by name.

    - **name**: Name of the user (mandatory)
    """
    query_search = "SELECT * FROM users WHERE nombre = :nombre"
    values = {"nombre": name}
    return await database.fetch_all(query_search, values)


async def get_all_users() -> dict:
    """
    This endpoint allows you to get all users in the database.
    """
    query = "SELECT * FROM users ORDER BY id_users ASC"
    results = await database.fetch_all(query)
    return {"message": "All users", "data": results}


async def create_user(user: User, response: Response) -> dict:
    """
    This endpoint allows you to create a new user in the database.

    - **id**: DNI of the user (mandatory)
    - **nombre**: First name of the user (mandatory)
    - **password**: Password of the user (mandatory)
    """

    default_values = ["string", "", 0]

    for field in user.__fields__:
        if user.__getattribute__(field) in default_values:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return f"Field {field} cannot be empty"

    results = await get_user_by_name(user.nombre)

    if results:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return f"User with name: {user.nombre} already exists"

    query = "INSERT INTO users (nombre, password) VALUES (:nombre, :password)"
    values = {
        "nombre": user.nombre,
        "password": user.password,
    }

    await database.execute(query=query, values=values)
    return {"message": "User created successfully", "data": user.dict()}


async def update_user(user: UserUpdate, response: Response) -> dict:
    """
    This endpoint allows you to update the information of a user in the database.

    - **id**: DNI of the user (mandatory)
    - **nombre**: First name of the user (mandatory)
    - **password**: Password of the user (mandatory)

    """
    results = await get_user_by_id(user.id_users)

    if user.id_users in ["string", ""]:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return "User id cannot be empty"

    if not results:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"User with id: {user.id_users} not found"

    update_fields = {}

    default_values = ["string", 0]

    for field in user.__fields__:
        if field == "id_users":
            continue
        if user.__getattribute__(field) in default_values:
            continue

        update_fields[field] = user.__getattribute__(field)

    if not update_fields:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return f"No fields to update for user with id: {user.id_users}"

    set_query = ", ".join(f"{field} = :{field}" for field in update_fields)
    values = {"id_users": user.id_users, **update_fields}

    query = f"UPDATE users SET {set_query} WHERE id_users = :id_users"
    await database.execute(query=query, values=values)

    return f"User with id {user.id_users} updated successfully"


async def delete_user(user: DeleteUser, response: Response) -> dict:
    """
    This endpoint allows you to delete a user by id.

    - **id**: DNI of the user (mandatory)
    """
    results = await get_user_by_id(user.id_users)

    if user.id_users in ["string", ""]:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return "User id cannot be empty"

    if not results:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"User with id: {user.id_users} not found"

    delete_query = "DELETE FROM users WHERE id_users = :id_users"
    values = {"id_users": user.id_users}

    await database.execute(delete_query, values)
    response.status_code = status.HTTP_200_OK
    return f"User with id {user.id_users} deleted"

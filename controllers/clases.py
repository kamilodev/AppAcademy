# Importa las librerias necesarias.
from data.connection import database as database
from fastapi import status, Response, status, HTTPException
from data.Models import CreateClasses, Classes


async def get_classes_by_id(id_classes: int):
    """
    The function `get_classes_by_id` retrieves all rows from the `classes` table where the `id_classes`
    column matches the provided `id_classes` parameter.

    :param id_classes: The parameter `id_classes` is an integer that represents the ID of the classes
    you want to retrieve from the database
    :type id_classes: int
    :return: a record matching the requested id.
    """
    query = f"SELECT * FROM classes WHERE id_classes = {id_classes} "
    results = await database.fetch_all(query)
    return results


async def get_classes(id_classes: int, response: Response):
    """
    The function `get_classes` retrieves class information by ID and returns a response with the
    appropriate status code and message.

    :param id_classes: The `id_classes` parameter is an integer that represents the ID of the classes
    you want to retrieve. It is used as an input to the `get_classes_by_id` function to fetch the
    classes with the specified ID
    :type id_classes: int
    :param response: The `response` parameter is an instance of the `Response` class. It is used to set
    the status code of the HTTP response and return the response data
    :type response: Response
    :return: either a string "No classes found" if no classes are found, or a dictionary with the keys
    "message" and "data" if classes are found. The value of "message" is "Classes found" and the value
    of "data" is the first element in the results list.
    """
    results = await get_classes_by_id(id_classes)

    if len(results) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"No classes found"
    else:
        response.status_code = status.HTTP_200_OK
        return {"message": "Classes found", "data": results[0]}


async def get_all_classes():
    """
    The function `get_all_classes` retrieves all classes from a database and returns them as a
    dictionary.
    :return: a dictionary with two keys: "mensaje" and "data". The value of "mensaje" is the string "All
    classes", and the value of "data" is the results of the database query, which is a list of all the
    classes.
    """
    query = "SELECT * FROM classes"
    results = await database.fetch_all(query)
    return {"mensaje": "All classes", "data": results}


async def create_classes(classes: CreateClasses):
    """
    The `create_classes` function allows the creation of a new class by inserting its name and pack ID
    into the database.

    :param classes: The parameter `classes` is of type `CreateClasses`. It is an object that contains
    the following attributes:
    :type classes: CreateClasses
    :return: a dictionary with the key "mensaje" and the value "classes created successfully".
    """
    query = f"INSERT INTO classes (name, id_packs) VALUES (:name, :id_packs)"
    values = {
        "name": classes.name,
        "id_packs": classes.id_packs,
    }
    await database.execute(query=query, values=values)

    return {"mensaje": "classes created successfully"}


async def update_classes(classes: Classes, response: Response):
    """
    The function `update_classes` updates the fields of a class object in a database table called
    "classes" based on the provided input.

    :param classes: The `classes` parameter is an instance of the `Classes` class, which contains the
    following attributes:
    :type classes: Classes
    :param response: The `response` parameter is an instance of the `Response` class. It is used to set
    the status code of the HTTP response
    :type response: Response
    :return: a string message indicating the result of the update operation. The possible return
    messages are:
    """

    result = await get_classes_by_id(classes.id_classes)

    if len(result) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"Clases with id: {classes.id_classes} not found"

    update_fields = {}

    if classes.id_classes != "int":
        update_fields["id_classes"] = classes.id_classes
    if classes.name != "str":
        update_fields["name"] = classes.name
    if classes.id_packs != "int":
        update_fields["id_packs"] = classes.id_packs

    if len(update_fields) == 0:
        return f"No fields to update for classes with id: {classes.id_classes}"

    if classes.name == "" or classes.name == "string":
        response.status_code = status.HTTP_400_BAD_REQUEST
        return f"Classes id cannot be empty"

    if not classes.id_packs or classes.id_packs == "int":
        response.status_code = status.HTTP_400_BAD_REQUEST
        return f"The field id_packs cannot be empty must contain an integer 1,2 or 3."

    id_packs = int(classes.id_packs)

    if id_packs not in [1, 2, 3]:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return f"The id_packs field must be an integer and only values 1, 2, and 3 are allowed."

    set_query = ", ".join(f"{field} =:{field}" for field in update_fields)
    values = {"id_classes": classes.id_classes, **update_fields}

    query = f"UPDATE classes SET {set_query} WHERE id_classes = :id_classes"
    await database.execute(query=query, values=values)

    return f"Classes with id {classes.id_classes} update successfully"


# Que no me deje eliminar una clase que tenga relacion con curso y que me deje un mensaje de aviso.
async def delete_classes(id_classes: int, response: Response):
    """
    The function `delete_classes` deletes a class from a database based on its ID and returns a response
    indicating whether the deletion was successful or not.

    :param id_classes: The `id_classes` parameter is an integer that represents the ID of the classes
    that need to be deleted. It is used to identify the specific classes that should be deleted from the
    database
    :type id_classes: int
    :param response: The `response` parameter is an instance of the `Response` class. It is used to set
    the status code of the HTTP response that will be returned by the function
    :type response: Response
    :return: a string message indicating whether the class with the given ID was found and deleted
    successfully or not.
    """

    results = await get_classes_by_id(id_classes)

    if len(results) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"Class with id: {id_classes} not found"

    delete_query = f"DELETE FROM classes WHERE id_classes = {id_classes}"
    await database.execute(delete_query)

    response.status_code = status.HTTP_200_OK
    return f"Classes with id {id_classes} deleted "

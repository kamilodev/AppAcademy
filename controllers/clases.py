# Importa las librerias necesarias.
from data.connection import database as database
from fastapi import status, Response, status, HTTPException
from data.Models import CreateClasses, Classes

async def get_classes_by_id(id_classes: int):
    query= f"SELECT * FROM classes WHERE id_classes = {id_classes} "
    results = await database.fetch_all(query)
    return results

async def get_classes(id_classes: int, response: Response):
    
    results = await get_classes_by_id(id_classes)
        
    if len(results) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"No classes found"
    else:
        response.status_code = status.HTTP_200_OK
        return {"message": "Classes found", "data": results[0]}


async def get_all_classes():
    """
    This enpoint allows you to get all classes in the database.
    
    """
    query = "SELECT * FROM classes"
    results = await database.fetch_all(query)
    return {"mensaje": "All classes", "data": results}


async def create_classes(classes: CreateClasses):
    """
    In this endpoint it allows us to create a new class by putting
     
    - **name**: Nombre de la clase.
    """
    query = f"INSERT INTO classes (name, id_packs) VALUES (:name, :id_packs)"
    values = {
        "name": classes.name,
        "id_packs": classes.id_packs,
    }
    await database.execute(query=query, values=values)
    
    return {"mensaje": "classes created successfully"}

# TODO: Validate if familiar exists
async def update_classes(classes: Classes, response: Response):
    """
    This endpoint allows you to update 
    the information of a classes in the database.

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
    
    if classes.name == "" or classes.name  == "string":
        response.status_code = status.HTTP_400_BAD_REQUEST
        return f"Classes id cannot be empty"
    
    if not classes.id_packs or classes.id_packs == "int":
        response.status_code = status.HTTP_400_BAD_REQUEST
        return f"The field id_packs cannot be empty must contain an integer 1,2 or 3."

    id_packs = int(classes.id_packs)
    
    if id_packs not in [1, 2, 3]:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return f"The id_packs field must be an integer and only values 1, 2, and 3 are allowed."

    set_query = ', '.join(f'{field} =:{field}' for field in update_fields)
    values = {"id_classes": classes.id_classes, **update_fields}
    
    query = f"UPDATE classes SET {set_query} WHERE id_classes = :id_classes"
    await database.execute(query = query, values =values)
    
    return f"Classes with id {classes.id_classes} update successfully"
 
# Que no me deje eliminar una clase que tenga relacion con curso y que me deje un mensaje de aviso.
async def delete_classes(id_classes: int, response:Response):
    """
    This endpoint allows you to delete 
    a classes in the database.
    
    """
    results = await get_classes_by_id(id_classes)
    
    if len(results) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"Class with id: {id_classes} not found"
    
    delete_query = f"DELETE FROM classes WHERE id_classes = {id_classes}"
    await database.execute(delete_query)
    
    response.status_code = status.HTTP_200_OK
    return f"Classes with id {id_classes} deleted "
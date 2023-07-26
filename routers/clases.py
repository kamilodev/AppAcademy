
# Importamos las librerias necesarias
from fastapi import APIRouter, Response, status, HTTPException
from data.Models import CreateClasses, Classes
from controllers import clases

# Creamos un objeto 
router = APIRouter(prefix="/classes", tags=["classes"])


# Creo un enrutador de forma get, que me devuelve una lista de clases
@router.get("/")
async def get_all_classes():
# Intento obtener los datos de la base de datos.    
    try:
        return await clases.get_all_classes()
# Si da un error, lo cojo y genero una excepción HTTP con el código 200 y el mensaje de error.        
    except Exception as e:
        raise HTTPException(status_code= 200, detail=str(e))
# Devuelve la lista de clases return Response(clases)

@router.get("/{id_classes}")
async def get_classes(id_classes: int, response: Response):
# Intento obtener los datos de la base de datos.    
    try:
        return await clases.get_classes(id_classes, response)
# Si da un error, lo cojo y genero una excepción HTTP con el código 200 y el mensaje de error.        
    except Exception as e:
        raise HTTPException(status_code= 200, detail=str(e))
    
    
# Creo un enrutador de forma post, que me crea una nueva clase.
@router.post("/create/")
async def create_classes(classes: CreateClasses):
# Intento crear una nueva clase en la base de datos
    try:
       return await clases.create_classes(classes)       
    except Exception as e:
# Si da un error, lo cojo y genero una excepción HTTP con el código 200 y el mensaje de error.
        raise HTTPException(status_code=200, detail=str(e))
    

# Creo un metodo que me actualiza la clase
@router.put("/update/")
async def update_classes(classes: Classes, response: Response ):
    try:
# Intento actualizar una clase 
       return await clases.update_classes(classes, response)
    except Exception as e:
# Si da un error, lo cojo y genero una excepción HTTP con el código 200 y el mensaje de error.
        raise HTTPException(status_code= 500, detail=str(e))
@router.delete("/delete/{id_classes}")
async def delete_classes(id_classes: int, response: Response):
    try:
# Intento eliminar una clase
        return await clases.delete_classes(id_classes, response)
    except Exception as e:
# Si da un error, lo cojo y genero una excepción HTTP con el código 200 y el mensaje de error.
        raise HTTPException(status_code= 200, detail=str(e))
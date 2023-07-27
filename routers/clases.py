# Importamos las librerias necesarias
from fastapi import APIRouter, Response, status, HTTPException
from data.Models import CreateClasses, Classes
from controllers import clases


router = APIRouter(prefix="/classes", tags=["classes"])


@router.get("/")
async def get_all_classes():
    try:
        return await clases.get_all_classes()
    except Exception as e:
        raise HTTPException(status_code=200, detail=str(e))


@router.get("/{id_classes}")
async def get_classes(id_classes: int, response: Response):
    try:
        return await clases.get_classes(id_classes, response)
    except Exception as e:
        raise HTTPException(status_code=200, detail=str(e))


@router.post("/create/")
async def create_classes(classes: CreateClasses):
    try:
        return await clases.create_classes(classes)
    except Exception as e:
        raise HTTPException(status_code=200, detail=str(e))


@router.put("/update/")
async def update_classes(classes: Classes, response: Response):
    try:
        return await clases.update_classes(classes, response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/delete/{id_classes}")
async def delete_classes(id_classes: int, response: Response):
    try:
        return await clases.delete_classes(id_classes, response)
    except Exception as e:
        raise HTTPException(status_code=200, detail=str(e))

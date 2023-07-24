from fastapi import APIRouter, Response, status
from data.Models import CreateLevel, Level
from controllers import levels

router = APIRouter(prefix="/levels", tags=["Levels"])


@router.get(
    "/",
    summary="Get all levels",
    response_description="All levels in database shown",
    status_code=status.HTTP_200_OK,
)
async def get_all_levels(response: Response):
    return await levels.get_all_levels(response)


@router.get(
    "/{id_levels}",
    summary="Get a level by id",
    response_description="Search a level by id",
    status_code=status.HTTP_200_OK,
)
async def get_level(id_levels: int, response: Response):
    return await levels.get_level(id_levels, response)


@router.post(
    "/create/",
    summary="Create a new level",
    response_description="A new level will be created in database",
    status_code=status.HTTP_201_CREATED,
)
async def create_level(level: CreateLevel):
    return await levels.create_level(level)


@router.put(
    "/update/",
    summary="Update a level",
    response_description="A level will be updated in database",
    status_code=status.HTTP_200_OK,
)
async def update_level(level: Level, response: Response):
    return await levels.update_level(level, response)


@router.delete(
    "/delete/{id_levels}",
    summary="Delete a level by id",
    response_description="A level will be deleted in database",
    status_code=status.HTTP_200_OK,
)
async def delete_level(id_levels: int, response: Response):
    return await levels.delete_level(id_levels, response)

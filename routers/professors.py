from fastapi import APIRouter, Response, status
from data.Models import DeleteProfessor, Professor
from controllers import professors

router = APIRouter(prefix="/professors", tags=["Professors"])


@router.get(
    "/",
    summary="Get all professors",
    response_description="All professors in database shown",
    status_code=status.HTTP_200_OK,
)
async def get_all_professors():
    return await professors.get_all_professors()


@router.get(
    "/{id_professors}",
    summary="Get a professor by id",
    response_description="Search a professor by id",
    status_code=status.HTTP_200_OK,
)
async def get_professor(id_professors: int, response: Response):
    return await professors.get_professor(id_professors, response)


@router.post(
    "/create/",
    summary="Create a new professor",
    response_description="A new professor will be created in database",
    status_code=status.HTTP_201_CREATED,
)
async def create_professor(professor: Professor, response: Response):
    return await professors.create_professor(professor, response)


@router.put(
    "/update/",
    summary="Update a professor",
    response_description="A professor will be updated in database",
    status_code=status.HTTP_200_OK,
)
async def update_professor(professor: Professor, response: Response):
    return await professors.update_professor(professor, response)


@router.delete(
    "/delete/{id_professors}",
    summary="Delete a professor by id",
    response_description="A professor will be deleted in database",
    status_code=status.HTTP_200_OK,
)
async def delete_professor(professor: DeleteProfessor, response: Response):
    return await professors.delete_professor(professor, response)

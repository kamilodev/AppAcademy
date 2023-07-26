from fastapi import APIRouter, Response, status
from controllers import inscriptions
from data.Models import Inscription, UpdateInscription
from data.Models import InscriptionDetail
from typing import List

router = APIRouter(prefix="/inscriptions", tags=["Inscriptions"])


@router.get(
    "/",
    summary="Get all inscriptions",
    response_description="All inscriptions in database shown",
    status_code=status.HTTP_200_OK,
)
async def get_all_inscriptions(response: Response):
    return await inscriptions.get_all_inscriptions(response)


@router.get(
    "/{id_inscriptions}",
    summary="Get a inscription by id",
    response_description="Search a inscription by id",
    status_code=status.HTTP_200_OK,
)
async def get_inscription(id_inscriptions: int, response: Response):
    return await inscriptions.get_inscription(id_inscriptions, response)


@router.get(
    "/student/{id_students}",
    summary="Get all inscriptions by student id",
    response_description="All inscriptions in database shown by student id",
    status_code=status.HTTP_200_OK,
)
async def get_inscription_by_id_student(id_students: str, response: Response):
    return await inscriptions.get_inscription_by_id_student(id_students, response)


@router.get(
    "/payments/{id_students}",
    summary="Get all payments by student id",
    response_description="All payments in database shown by student id",
    status_code=status.HTTP_200_OK,
)
async def get_payments_by_student(id_students: str, response: Response):
    return await inscriptions.get_payments_by_student(id_students, response)


@router.post(
    "/create/",
    summary="Create a new inscription",
    response_description="A new inscription will be created in database",
    status_code=status.HTTP_201_CREATED,
)
async def create_inscription(
    inscription: Inscription,
    inscriptions_detail: List[InscriptionDetail],
    response: Response,
):
    return await inscriptions.create_inscription(
        inscription, inscriptions_detail, response
    )


@router.put(
    "/update/",
    summary="Update a inscription",
    response_description="A inscription will be updated in database",
    status_code=status.HTTP_200_OK,
)
async def update_inscription(update: UpdateInscription, response: Response):
    return await inscriptions.update_inscription(update, response)


@router.delete(
    "/delete/{id_inscriptions}",
    summary="Delete a inscription by id",
    response_description="A inscription will be deleted in database",
    status_code=status.HTTP_200_OK,
)
async def delete_inscription(id_inscriptions: int, response: Response):
    return await inscriptions.delete_inscription(id_inscriptions, response)

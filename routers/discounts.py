from fastapi import APIRouter, Response, status
from data.Models import DeleteDiscount, Discount
from controllers import discounts

router = APIRouter(prefix="/discounts", tags=["Discounts"])


@router.get(
    "/",
    summary="Get all discounts",
    response_description="All discounts in database shown",
    status_code=status.HTTP_200_OK,
)
async def get_all_discounts():
    return await discounts.get_all_discounts()


@router.get(
    "/{id_discounts}",
    summary="Get a disscount by id",
    response_description="Search a discount by id",
    status_code=status.HTTP_200_OK,
)
async def get_discount(id_discounts: int, response: Response):
    return await discounts.get_discount(id_discounts, response)


@router.post(
    "/create/",
    summary="Create a new discount",
    response_description="A new discount will be created in database",
    status_code=status.HTTP_201_CREATED,
)
async def create_discount(discount: Discount, response: Response):
    return await discounts.create_discount(discount, response)


@router.put(
    "/update/",
    summary="Update a discount",
    response_description="A discount will be updated in database",
    status_code=status.HTTP_200_OK,
)
async def update_discount(discount: Discount, response: Response):
    return await discounts.update_discount(discount, response)


@router.delete(
    "/delete/{id_discounts}",
    summary="Delete a discount by id",
    response_description="A discount will be deleted in database",
    status_code=status.HTTP_200_OK,
)
async def delete_discount(discount: DeleteDiscount, response: Response):
    return await discounts.delete_discount(discount, response)
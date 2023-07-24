from fastapi import APIRouter, Response, status
from data.Models import DeleteUser, User
from controllers import users

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/",
    summary="Get all users",
    response_description="All users in database shown",
    status_code=status.HTTP_200_OK,
)
async def get_all_users():
    return await users.get_all_users()


@router.get(
    "/{id_users}",
    summary="Get a user by id",
    response_description="Search a user by id",
    status_code=status.HTTP_200_OK,
)
async def get_user(id_users: int, response: Response):
    return await users.get_user(id_users, response)


@router.post(
    "/create/",
    summary="Create a new user",
    response_description="A new user will be created in database",
    status_code=status.HTTP_201_CREATED,
)
async def create_user(user: User, response: Response):
    return await users.create_user(user, response)


@router.put(
    "/update/",
    summary="Update a user",
    response_description="A user will be updated in database",
    status_code=status.HTTP_200_OK,
)
async def update_user(user: User, response: Response):
    return await users.update_user(user, response)


@router.delete(
    "/delete/{id_users}",
    summary="Delete a user by id",
    response_description="A user will be deleted in database",
    status_code=status.HTTP_200_OK,
)
async def delete_user(user: DeleteUser, response: Response):
    return await users.delete_user(user, response)
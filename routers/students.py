from fastapi import APIRouter, Response, status
from data.Models import DeleteStudent, Student, UpdateStudent
from controllers import students

router = APIRouter(prefix="/students", tags=["Students"])


@router.get(
    "/",
    summary="Get all students",
    response_description="All students in database shown",
    status_code=status.HTTP_200_OK,
)
async def get_all_students(response: Response):
    return await students.get_all_students(response)


@router.get(
    "/{id_students}",
    summary="Get a student by id",
    response_description="Search a student by id",
    status_code=status.HTTP_200_OK,
)
async def get_student(id_students: str, response: Response):
    return await students.get_student(id_students, response)


@router.post(
    "/create/",
    summary="Create a new student",
    response_description="A new student will be created in database",
    status_code=status.HTTP_201_CREATED,
)
async def create_student(student: Student, response: Response):
    return await students.create_student(student, response)


@router.put(
    "/update/",
    summary="Update a student",
    response_description="A student will be updated in database",
    status_code=status.HTTP_200_OK,
)
async def update_student(student: UpdateStudent, response: Response):
    return await students.update_student(student, response)


@router.delete(
    "/delete/{id_students}",
    summary="Delete a student by id",
    response_description="A student will be deleted in database",
    status_code=status.HTTP_200_OK,
)
async def delete_student(student: DeleteStudent, response: Response):
    return await students.delete_student(student, response)

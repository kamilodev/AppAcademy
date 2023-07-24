from fastapi import APIRouter, Response, status
from data.Models import NewCourses
from controllers import courses


router = APIRouter(prefix="/courses", tags=["Courses"])


@router.get(
    "/",
    summary="Get all courses",
    response_description="All courses in database shown",
    status_code=status.HTTP_200_OK,
)
async def get_all_courses(response: Response):
    return await courses.get_all_courses(response)


@router.get(
    "/{id_courses}",
    summary="Get a course by id",
    response_description="Search a course by id",
    status_code=status.HTTP_200_OK,
)
async def get_courses(id_course: int, response: Response):
    return await courses.get_courses(id_course, response)


@router.get(
    "/professor/{name_professor}",
    summary="Get all courses by professor name",
    response_description="All courses in database shown by professor name",
    status_code=status.HTTP_200_OK,
)
async def get_all_courses_by_professor(name_professor: str, response: Response):
    return await courses.get_all_courses_by_professor(name_professor, response)


@router.get(
    "/name/{name_course}",
    summary="Get a course by name",
    response_description="Search a course by name",
    status_code=status.HTTP_200_OK,
)
async def get_course_by_name(name_course: str, response: Response):
    return await courses.get_course_by_name(name_course, response)


@router.get(
    "/level/{level}",
    summary="Get all courses by level",
    response_description="All courses in database shown by level",
    status_code=status.HTTP_200_OK,
)
async def get_courses_by_level(level: str, response: Response):
    return await courses.get_courses_by_level(level, response)


@router.post(
    "/create/",
    summary="Create a new course",
    response_description="A new course will be created in database",
    status_code=status.HTTP_201_CREATED,
)
async def create_course(course: NewCourses, response: Response):
    return await courses.create_course(course, response)


@router.put(
    "/update/",
    summary="Update a course",
    response_description="A course will be updated in database",
    status_code=status.HTTP_200_OK,
)
async def update_course(course: NewCourses, response: Response):
    return await courses.update_course(course, response)


@router.delete(
    "/delete/{id_courses}",
    summary="Delete a course by id",
    status_code=status.HTTP_200_OK,
)
async def delete_course(id_courses: int, response: Response):
    return await courses.delete_course(id_courses, response)

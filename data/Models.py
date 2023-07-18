from pydantic import BaseModel


class Student(BaseModel):
    id_students: str
    first_name: str
    last_name: str
    phone: str
    email: str
    age: int
    id_familiar: int
    status: bool


class DeleteStudent(BaseModel):
    id_students: str


class Professor(BaseModel):
    id_professors: str
    first_name: str
    last_name: str
    phone: str
    email: str

class Courses(BaseModel):
    id_courses: int
    id_classes: int
    id_levels: int
    id_professors: int
    max_students: int
    prices: int


class NewCourses(BaseModel):
    id_courses: int
    name_class: str
    level: str
    name_professor: str
    max_students: int
    prices: int

class CreateLevel(BaseModel):
    name: str


class Level(BaseModel):
    id_levels: int
    name: str

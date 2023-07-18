from pydantic import BaseModel


class Student(BaseModel):
    id_students: str
    first_name: str
    last_name: str
    phone: str
    email: str
    age: int
    id_familiar: str
    status: bool='False'


class Professor(BaseModel):
    id_professors: str
    first_name: str
    last_name: str
    phone: str
    email: str


class CreateLevel(BaseModel):
    name: str


class Level(BaseModel):
    id_levels: int
    name: str
    
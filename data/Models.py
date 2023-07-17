from pydantic import BaseModel


class Student(BaseModel):
    id_students: int
    first_name: str
    last_name: str
    phone: str
    email: str
    age: int
    id_familiar: int


class Professor(BaseModel):
    id_professors: int
    first_name: str
    last_name: str
    phone: str
    email: str
    address: str

class Level(BaseModel):
    id_levels: int
    name: str
    
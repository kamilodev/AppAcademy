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


class Classes(BaseModel):
    id_classes: int
    name: str
    id_packs: int
    
class CreateClasses(BaseModel):
    name: str
    id_packs: int
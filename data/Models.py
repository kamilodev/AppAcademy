from pydantic import BaseModel


class Student(BaseModel):
    id_students: str
    first_name: str
    last_name: str
    phone: str
    email: str
    age: int
    id_familiar: str
    status: bool


class UpdateStudent(BaseModel):
    id_students: str
    first_name: str
    last_name: str
    phone: str
    email: str
    age: int
    status: bool


class DeleteStudent(BaseModel):
    id_students: str


class Professor(BaseModel):
    id_professors: str
    first_name: str
    last_name: str
    phone: str
    email: str


class Classes(BaseModel):
    id_classes: int
    name: str
    id_packs: int
    
class CreateClasses(BaseModel):
    name: str
    id_packs: int



class DeleteProfessor(BaseModel):
    id_professors: str


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


class User(BaseModel):
    id_users: str
    nombre: str
    password: str


class DeleteUser(BaseModel):
    id_users: str
      
class Inscription(BaseModel):
    id_students: str
    observation: str


class InscriptionDetail(BaseModel):
    id_courses: int


class UpdateInscription(BaseModel):
    id_inscriptions: int
    id_courses: int
    status: bool

<<<<<<< HEAD

class Discount(BaseModel):
    id_discounts: int
    discounts: int


class DeleteDiscount(BaseModel):
    id_discounts: int
=======
>>>>>>> 31ff1eea0c890dcb1c5219c5c146e07c33ece578

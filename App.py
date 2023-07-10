from fastapi import FastAPI
from dotenv import load_dotenv
from Models import Student
import databases
import os

load_dotenv()

app = FastAPI()
database = databases.Database(os.environ["MYSQL_ADDON_URI"])


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.post("/students")
async def create_student(student: Student):
    query = f"INSERT INTO students (id_students, first_name, last_name, phone, email, age, id_familiar) VALUES (:id_students, :first_name, :last_name, :phone, :email, :age, :id_familiar)"
    values = {
        "id_students": student.id_students,
        "first_name": student.first_name,
        "last_name": student.last_name,
        "phone": student.phone,
        "email": student.email,
        "age": student.age,
        "id_familiar": student.id_familiar,
    }
    await database.execute(query=query, values=values)

    return {"message": "Student created successfully"}


@app.get("/")
async def first_api():
    query = "SELECT * FROM students"
    results = await database.fetch_all(query)
    return {"message": "Hello World", "data": results}

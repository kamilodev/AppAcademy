import pytest
from pytest_mock import mocker
from controllers.students import get_student_by_id
from fastapi import Response, status

student = {
    "id_students": "12345678",
    "first_name": "John",
    "last_name": "Doe",
    "phone": "1234567890",
    "email": "johndoe@example.com",
    "age": 25,
    "id_familiar": None,
    "status": 1,
    "familiar": None,
}


@pytest.mark.asyncio
async def test_retrieve_valid_student(mocker):
    mocker.patch(
        "data.connection.database.fetch_all",
        return_value=[student],
    )
    result = await get_student_by_id("12345676")
    assert len(result) == 1
    assert result[0]["id_students"] == "12345678"
    assert result[0]["first_name"] == "John"
    assert result[0]["last_name"] == "Doe"
    assert result[0]["phone"] == "1234567890"
    assert result[0]["email"] == "johndoe@example.com"
    assert result[0]["age"] == 25
    assert result[0]["id_familiar"] is None
    assert result[0]["status"] == 1
    assert result[0]["familiar"] is None


@pytest.mark.asyncio
async def test_retrieve_invalid_student(mocker):
    id_students = "12345676"
    mocker.patch(
        "data.connection.database.fetch_all",
        return_value=[
            {
                "message": f"Student with id {id_students} not found",
            }
        ],
    )
    response = Response()
    result = await get_student_by_id("12345676")
    assert result[0]["message"] == f"Student with id {id_students} not found"

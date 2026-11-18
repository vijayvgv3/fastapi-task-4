from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import json
from pathlib import Path

app = FastAPI()

DATA_FILE = Path(__file__).parent / "employees.json"


class Employee(BaseModel):
    name: str = Field(min_length=1)
    salary: float = Field(gt=0)


def read_employees():
    with open(DATA_FILE, "r") as file:
        return json.load(file)


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/employees")
def get_employees():
    return read_employees()


@app.get("/employees/{name}")
def get_employee(name: str):
    employees = read_employees()

    for employee in employees:
        if employee["name"].lower() == name.lower():
            return employee

    raise HTTPException(status_code=404, detail="Employee not found")


@app.post("/employees")
def create_employee(employee: Employee):
    employees = read_employees()
    employees.append(employee.model_dump())

    with open(DATA_FILE, "w") as file:
        json.dump(employees, file, indent=4)

    return employee
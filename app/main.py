# app/main.py
from fastapi import FastAPI
from app.fake_db import students, _class

app = FastAPI()

@app.get("/")
def main_page():
    return {"detail": "students api is running..."}

@app.get("/students")
def list_students():
    return students

@app.get("/class")
def list_class():
    return _class


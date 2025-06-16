# app/main.py
from fastapi import FastAPI
from app.fake_db import students

app = FastAPI()

@app.get("/students")
def list_students():
    return students
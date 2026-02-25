
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class RegisterRequest(BaseModel):
    email: str
    password: str

@app.post("/auth/register")
def register(request: RegisterRequest):
    return {"status": "ok", "message": f"User {request.email} registered successfully"}
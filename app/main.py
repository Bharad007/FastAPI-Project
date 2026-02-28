from fastapi import FastAPI
from .db.database import init_db
from .api import auth, expenses

app = FastAPI()

# create tables at startup
@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(auth.router)
app.include_router(expenses.router)
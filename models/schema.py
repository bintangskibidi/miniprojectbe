from pony.orm import Required, PrimaryKey
from app import db   # ⬅️ ambil db dari app.py

class User(db.Entity):
    id = PrimaryKey(int, auto=True)
    email = Required(str, unique=True)
    password = Required(str)
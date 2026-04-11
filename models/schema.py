from pony.orm import Database, Required, PrimaryKey
import bcrypt

db = Database()

class User(db.Entity):
    id = PrimaryKey(int, auto=True)
    email = Required(str, unique=True)
    password = Required(str) # Simpan hash bcrypt di sini

# Koneksi ke database sqlite kamu
db.bind(provider='sqlite', filename='../database.sqlite', create_db=True)
db.generate_mapping(create_tables=True)
import falcon
from falcon_cors import CORS
from pony.orm import Database, db_session
import bcrypt
import os
from dotenv import load_dotenv

# =====================
# LOAD ENV
# =====================
load_dotenv()

# =====================
# INIT DATABASE (MYSQL)
# =====================
db = Database()

db.bind(
    provider='mysql',
    host=os.getenv("HOST_DB"),
    user=os.getenv("USER_DB"),
    password=os.getenv("PASSWORD_DB"),
    database=os.getenv("DB_NAME"),
    port=int(os.getenv("PORT_DB"))
)

# =====================
# IMPORT MODEL (SETELAH DB)
# =====================
from models.schema import User

# =====================
# GENERATE TABLE
# =====================
db.generate_mapping(create_tables=True)


# =====================
# SEED USER
# =====================
@db_session
def seed_user():
    new_email = "admin@gmail.com"

    if not User.get(email=new_email):
        password_plain = "123456"
        hashed = bcrypt.hashpw(password_plain.encode('utf-8'), bcrypt.gensalt())

        User(email=new_email, password=hashed.decode('utf-8'))
        print(f"✅ User '{new_email}' otomatis dibuat!")
    else:
        print("ℹ️ User sudah ada.")


seed_user()

# =====================
# FALCON SETUP
# =====================
from resources.auth import LoginResource

cors = CORS(allow_all_origins=True, allow_all_headers=True, allow_all_methods=True)
app = falcon.App(middleware=[cors.middleware])

login_api = LoginResource()
app.add_route('/auth/login', login_api)
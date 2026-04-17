import falcon
from falcon_cors import CORS
from pony.orm import db_session
import bcrypt
from resources.auth import LoginResource
from models.schema import User # Pastikan User diimport

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

# Panggil fungsinya supaya jalan pas aplikasi mulai
seed_user()
# --- SETUP FALCON ---
cors = CORS(allow_all_origins=True, allow_all_headers=True, allow_all_methods=True)
app = falcon.App(middleware=[cors.middleware])

# Routing
login_api = LoginResource()
app.add_route('/auth/login', login_api)
import falcon
import jwt
import bcrypt
from datetime import datetime, timedelta
from pony.orm import db_session, select
from models.schema import User
from util.response import send_response

SECRET_KEY = "NabilGantengSekali"

class LoginResource:
    @db_session
    def on_post(self, req, resp):
        try:
            # GANTI BAGIAN INI: Pakai req.media, bukan req.get_json()
            data = req.media 
            email = data.get('email')
            password = data.get('password')

            if not email or not password:
                send_response(resp, falcon.HTTP_400, "Email dan password wajib diisi!")
                return

            user = select(u for u in User if u.email == email).first()

            if not user or not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                send_response(resp, falcon.HTTP_401, "Email atau Password salah!")
                return

            payload = {
                "user_id": user.id,
                "exp": datetime.utcnow() + timedelta(hours=24)
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

            send_response(resp, falcon.HTTP_200, "Login Berhasil!", {"token": token})

        except Exception as e:
            # Biar gampang debug, kita kirim pesan error aslinya
            send_response(resp, falcon.HTTP_500, f"Terjadi kesalahan: {str(e)}")
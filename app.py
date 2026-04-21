import falcon
from falcon_cors import CORS  # Import sudah benar
from pony.orm import db_session
from database import db
import json
from datetime import date, datetime
import bcrypt

def json_serializer(obj):
    if isinstance(obj, (date, datetime)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

cors = CORS(
    allow_origins_list=['http://localhost:5173', 'http://127.0.0.1:5173'],
    allow_all_headers=True,
    allow_all_methods=True
)

db.bind(
    provider='mysql',
    host='localhost',
    user='root',
    password='',
    database='miniprojectbe',
    port=3306
)

from models.schema import User, Siswa
db.generate_mapping(create_tables=True)

from resources.auth import LoginResource
from resources.siswa import SiswaResource, DetailSiswaResource

# Masukkan middleware CORS ke sini!
app = falcon.App(middleware=[cors.middleware]) 
app.resp_options.media_handlers[falcon.MEDIA_JSON] = falcon.media.JSONHandler(
    dumps=lambda obj: json.dumps(obj, default=json_serializer)
)

app.add_route('/auth/login', LoginResource())
app.add_route('/siswa', SiswaResource())
app.add_route('/siswa/{id:int}', DetailSiswaResource())
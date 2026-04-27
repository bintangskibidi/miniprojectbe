import json
from datetime import date, datetime

import falcon
from falcon_cors import CORS
from database import db

def json_serializer(obj):
    if isinstance(obj, (date, datetime)):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


# =========================
# CORS CONFIG
# =========================
cors = CORS(
    allow_all_origins=True,
    allow_all_headers=True,
    allow_all_methods=True
)


# =========================
# DATABASE CONFIG
# =========================
db.bind(
    provider='mysql',
    host='localhost',
    user='root',
    password='',
    database='miniprojectbe',
    port=3306
)


# =========================
# IMPORT MODELS
# =========================
from models.schema import (
    User,
    Siswa,
    Jurusan,
    Kelas,
    TahunAjaran,
    AspekPenilaian
)

db.generate_mapping(create_tables=True)


# =========================
# IMPORT RESOURCES
# =========================
from resources.auth import LoginResource
from resources.siswa import SiswaResource, DetailSiswaResource
from resources.kelas import KelasResource
from resources.jurusan import JurusanResource
from resources.tahunajaran import TahunAjaranResource
from resources.aspekpenilaian import AspekPenilaianResource


# =========================
# FALCON APP
# =========================
app = falcon.App(middleware=[cors.middleware])

app.resp_options.media_handlers[falcon.MEDIA_JSON] = falcon.media.JSONHandler(
    dumps=lambda obj: json.dumps(obj, default=json_serializer)
)


# =========================
# RESOURCE INSTANCES
# =========================
kelas_api = KelasResource()
jurusan_api = JurusanResource()
tahunajaran_api = TahunAjaranResource()
aspekpenilaian_api = AspekPenilaianResource()


# =========================
# ROUTES
# =========================
app.add_route('/auth/login', LoginResource())

# Siswa
app.add_route('/siswa', SiswaResource())
app.add_route('/siswa/{id:int}', DetailSiswaResource())

# Kelas
app.add_route('/kelas', kelas_api)
app.add_route('/kelas/{id:int}', kelas_api)

# Jurusan
app.add_route('/jurusan', jurusan_api)
app.add_route('/jurusan/{id:int}', jurusan_api)

# Tahun Ajaran
app.add_route('/tahun-ajaran', tahunajaran_api)
app.add_route('/tahun-ajaran/{id:int}', tahunajaran_api)

# Aspek Penilaian
app.add_route('/aspek-penilaian', aspekpenilaian_api)
app.add_route('/aspek-penilaian/{id:int}', aspekpenilaian_api)
app.add_route('/jurusan/{id}', jurusan_api)
app.add_route('/walikelas', walikelas_api)
app.add_route('/walikelas/{id:int}', walikelas_detail_api)

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
    AspekPenilaian,
    JenisSemester,
    Semester
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
from resources.walikelas import WaliKelasResource, DetailwalikelasResource
from resources.jenissemester import JenisSemesterResource
from resources.semester import SemesterResource



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
tahun_ajaran_api = TahunAjaranResource()
aspekpenilaian_api = AspekPenilaianResource()
walikelas_api = WaliKelasResource ()
walikelas_detail_api = DetailwalikelasResource ()
jenis_semester_api = JenisSemesterResource()
semester_api = SemesterResource()


# =========================
# ROUTES
# =========================
app.add_route('/auth/login', LoginResource())

app.add_route('/siswa', SiswaResource())
app.add_route('/siswa/{id:int}', DetailSiswaResource())

app.add_route('/kelas', kelas_api)
app.add_route('/kelas/{id:int}', kelas_api)

app.add_route('/jurusan', jurusan_api)
app.add_route('/jurusan/{id:int}', jurusan_api)

app.add_route('/tahun-ajaran', tahun_ajaran_api)
app.add_route('/tahun-ajaran/{id:int}', tahun_ajaran_api)

app.add_route('/aspek-penilaian', aspekpenilaian_api)
app.add_route('/aspek-penilaian/{id:int}', aspekpenilaian_api)

app.add_route('/walikelas', walikelas_api)
app.add_route('/walikelas/{id:int}', walikelas_detail_api)

app.add_route('/jenis-semester', jenis_semester_api)
app.add_route('/jenis-semester/{id:int}', jenis_semester_api)

app.add_route('/semester', semester_api)
app.add_route('/semester/{id:int}', semester_api)

import json
from datetime import date, datetime

import falcon
from database import db


# =========================
# JSON SERIALIZER
# =========================
def json_serializer(obj):
    if isinstance(obj, (date, datetime)):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


# =========================
# CORS MIDDLEWARE
# =========================
class SimpleCORS:
    def process_request(self, req, resp):
        resp.set_header("Access-Control-Allow-Origin", "*")
        resp.set_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        resp.set_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")

        if req.method == "OPTIONS":
            resp.status = falcon.HTTP_200
            resp.complete = True


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
from resources.siswa import (
    SiswaResource,
    SiswaDropdownResource,
    DetailSiswaResource
)
from resources.kelas import KelasResource
from resources.jurusan import JurusanResource
from resources.tahunajaran import TahunAjaranResource
from resources.aspekpenilaian import AspekPenilaianResource
from resources.walikelas import WaliKelasResource, DetailwalikelasResource
from resources.jenissemester import JenisSemesterResource
from resources.mapel import MapelResource
from resources.semester import SemesterResource
from resources.ekstra import EkstraKulikulerResource, DetailekstrakurikulerResource


# =========================
# APP INIT
# =========================
app = falcon.App(middleware=[SimpleCORS()])

app.resp_options.media_handlers[falcon.MEDIA_JSON] = falcon.media.JSONHandler(
    dumps=lambda obj: json.dumps(obj, default=json_serializer)
)


# =========================
# RESOURCE INSTANCES
# =========================
siswa_api = SiswaResource()
siswa_dropdown_api = SiswaDropdownResource()
kelas_api = KelasResource()
jurusan_api = JurusanResource()
tahun_ajaran_api = TahunAjaranResource()
aspekpenilaian_api = AspekPenilaianResource()
walikelas_api = WaliKelasResource()
walikelas_detail_api = DetailwalikelasResource()
jenis_semester_api = JenisSemesterResource()
mapel_api = MapelResource()
semester_api = SemesterResource()
ekstrakurikuler_api = EkstraKulikulerResource()
ekstrakurikuler_detail_api = DetailekstrakurikulerResource()


# =========================
# ROUTES
# =========================
app.add_route('/auth/login', LoginResource())

app.add_route('/siswa', siswa_api)
app.add_route('/siswa/dropdown', siswa_dropdown_api)
app.add_route('/siswa/{id:int}', DetailSiswaResource())

app.add_route('/kelas', kelas_api)
app.add_route('/kelas/{id:int}', kelas_api)

app.add_route('/jurusan', jurusan_api)
app.add_route('/jurusan/{id:int}', jurusan_api)

app.add_route('/tahun-ajaran', tahun_ajaran_api)
app.add_route('/tahun-ajaran/{id:int}', tahun_ajaran_api)

app.add_route('/ekstra', ekstrakurikuler_api)
app.add_route('/ekstra/{id:int}', ekstrakurikuler_detail_api)

app.add_route('/aspek-penilaian', aspekpenilaian_api)
app.add_route('/aspek-penilaian/{id:int}', aspekpenilaian_api)

app.add_route('/walikelas', walikelas_api)
app.add_route('/walikelas/{id:int}', walikelas_detail_api)

app.add_route('/jenis-semester', jenis_semester_api)
app.add_route('/jenis-semester/{id:int}', jenis_semester_api)

app.add_route('/mapel', mapel_api)
app.add_route('/mapel/{id:int}', mapel_api)

app.add_route('/semester', semester_api)
app.add_route('/semester/{id:int}', semester_api)

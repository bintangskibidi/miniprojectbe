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
# CORS MIDDLEWARE (FIX UTAMA)
# =========================
class SimpleCORS:
    def process_request(self, req, resp):
        resp.set_header("Access-Control-Allow-Origin", "*")
        resp.set_header("Access-Control-Allow-Headers", "*")
        resp.set_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")

        # HANDLE PREFLIGHT REQUEST
        if req.method == "OPTIONS":
            resp.status = falcon.HTTP_200
            resp.complete = True
            return


class SimpleCORS:
    def process_request(self, req, resp):
        resp.set_header("Access-Control-Allow-Origin", "*")
        resp.set_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        resp.set_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")

    def process_response(self, req, resp, resource, req_succeeded):
        # Penting untuk menangani request OPTIONS dari browser
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
    JenisSemester
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
from resources.ekstra import EkstraKulikulerResource, DetailekstrakurikulerResource


# =========================
# APP INIT (FIX DI SINI)
# =========================
app = falcon.App(middleware=[SimpleCORS()])

app.resp_options.media_handlers[falcon.MEDIA_JSON] = falcon.media.JSONHandler(
    dumps=lambda obj: json.dumps(obj, default=json_serializer)
)


# =========================
# RESOURCE INSTANCES
# =========================
kelas_api = KelasResource()
jurusan_api = JurusanResource()
ekstrakurikuler_api = EkstraKulikulerResource()
tahunajaran_api = TahunAjaranResource()
aspekpenilaian_api = AspekPenilaianResource()
walikelas_api = WaliKelasResource()
walikelas_detail_api = DetailwalikelasResource()
jenissemester_api = JenisSemesterResource()


# =========================
# ROUTES (INI SUDAH BENAR)
# =========================
app.add_route('/auth/login', LoginResource())

app.add_route('/siswa', SiswaResource())
app.add_route('/siswa/{id:int}', DetailSiswaResource())

app.add_route('/kelas', kelas_api)
app.add_route('/kelas/{id:int}', kelas_api)

app.add_route('/jurusan', jurusan_api)
app.add_route('/jurusan/{id:int}', jurusan_api)

app.add_route('/ekstra', EkstraKulikulerResource())
app.add_route('/ekstra/{id:int}', DetailekstrakurikulerResource())

app.add_route('/tahun-ajaran', tahunajaran_api)
app.add_route('/tahun-ajaran/{id:int}', tahunajaran_api)

app.add_route('/aspek-penilaian', aspekpenilaian_api)
app.add_route('/aspek-penilaian/{id:int}', aspekpenilaian_api)

app.add_route('/walikelas', walikelas_api)
app.add_route('/walikelas/{id:int}', walikelas_detail_api)

app.add_route('/jenis-semester', jenissemester_api)
app.add_route('/jenis-semester/{id:int}', jenissemester_api)
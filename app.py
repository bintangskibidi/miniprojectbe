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
    Pegawai,
    Siswa,
    Jurusan,
    Kelas,
    TahunAjaran,
    Presensi,
    AspekPenilaian,
    JenisSemester,
    Cuti,
    Lembur,
    KelolaKegiatan,
    Indikator,
    Surat,
    Peminjaman,
    Buku,
    Semester,
    InformasiLembaga,
    Banner,
    Raport,
    JadwalMengajar,
    Izin,
    BackupFile
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
from resources.backupdata import BackupDataResource
from resources.raport import RaportResource
from resources.presensi import PresensiResource
from resources.jadwalmengajar import JadwalMengajarResource, JadwalDropdownResource
from resources.pegawai import PegawaiResource
from resources.distribusijam import DistribusiJamResource
from resources.riwayatmengajar import RiwayatMengajarResource
from resources.databuku import DataBukuResource, DetailBukuResource
from resources.peminjamanbuku import DataPeminjamanResource, DetailPeminjamanResource
from resources.informasilembaga import InformasiLembagaResource, DetailInformasiLembagaResource
from resources.banneraplikasi import BannerAplikasiResource
from resources.settingabsensi import SettingAbsensiResource
from resources.kelolaindikator import SuratResource, IndikatorResource
from resources.kelolakegiatan import KelolaKegiatanResource, DetailKelolaKegiatanResource
from resources.cuti import CutiResource, DetailCutiResource
from resources.lembur import LemburResource, DetailLemburResource
from resources.izin import IzinResource, DetailIzinResource





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
databuku_api = DataBukuResource()
settingabsensi_api = SettingAbsensiResource()
informasilembaga_api = InformasiLembagaResource()
informasilembaga_detail_api = DetailInformasiLembagaResource()
izin_api = IzinResource()
izin_detail_api = DetailIzinResource()
lembur_api = LemburResource()
lembur_detail_api = DetailLemburResource()
cuti_api = CutiResource()
cuti_detail_api = DetailCutiResource()
kelolakegiatan_api = KelolaKegiatanResource()
kelolakegiatan_detail_api = DetailKelolaKegiatanResource()
databuku_detail_api = DetailBukuResource()
peminjaman_api = DataPeminjamanResource()
surat_api = SuratResource()
indikator_api = IndikatorResource()
backup_api = BackupDataResource()
banner_api = BannerAplikasiResource()
peminjaman_detail_api = DetailPeminjamanResource()
aspekpenilaian_api = AspekPenilaianResource()
presensi_api = PresensiResource()
walikelas_api = WaliKelasResource()
walikelas_detail_api = DetailwalikelasResource()
jenis_semester_api = JenisSemesterResource()
mapel_api = MapelResource()
semester_api = SemesterResource()
ekstrakurikuler_api = EkstraKulikulerResource()
ekstrakurikuler_detail_api = DetailekstrakurikulerResource()
raport_api = RaportResource()
jadwal_api = JadwalMengajarResource()
jadwal_dropdown_api = JadwalDropdownResource()

# =========================
# ROUTES
# =========================
app.add_route('/auth/login', LoginResource())

app.add_route('/siswa', siswa_api)
app.add_route('/siswa/dropdown', siswa_dropdown_api)
app.add_route('/siswa/{id:int}', DetailSiswaResource())

app.add_route('/kelas', kelas_api)
app.add_route('/kelas/{id:int}', kelas_api)

app.add_route('/settingabsensi', settingabsensi_api)
app.add_route('/settingabsensi/{id:int}', settingabsensi_api)


# Routing API Surat Menyurat
app.add_route('/surat', surat_api)
app.add_route('/surat/{id:int}', surat_api)

# Routing API Kelola Indikator Kinerja
app.add_route('/indikator', indikator_api)
app.add_route('/indikator/{id:int}', indikator_api)

app.add_route('/databuku', databuku_api)
app.add_route('/databuku/{id:int}', databuku_detail_api)

app.add_route('/izin', izin_api)
app.add_route('/izin/{id:int}', izin_detail_api)

app.add_route('/lembur', lembur_api)
app.add_route('/lembur/{id:int}', lembur_detail_api)

app.add_route('/cuti', cuti_api)
app.add_route('/cuti/{id:int}', cuti_detail_api)

app.add_route('/kelolakegiatan', kelolakegiatan_api)
app.add_route('/kelolakegiatan/{id:int}', kelolakegiatan_detail_api)

app.add_route('/informasilembaga', informasilembaga_api)
app.add_route('/informasilembaga/{id:int}', informasilembaga_detail_api)


app.add_route('/jurusan', jurusan_api)
app.add_route('/jurusan/{id:int}', jurusan_api)

app.add_route('/backup', backup_api)
app.add_route('/backup/{id:int}', backup_api)

app.add_route('/banner', banner_api)
app.add_route('/banner/{id:int}', banner_api)

app.add_route('/tahun-ajaran', tahun_ajaran_api)
app.add_route('/tahun-ajaran/{id:int}', tahun_ajaran_api)

app.add_route('/presensi', presensi_api)
app.add_route('/presensi/{id:int}', presensi_api)

app.add_route('/ekstra', ekstrakurikuler_api)
app.add_route('/ekstra/{id:int}', ekstrakurikuler_detail_api)

app.add_route('/aspek-penilaian', aspekpenilaian_api)
app.add_route('/aspek-penilaian/{id:int}', aspekpenilaian_api)

app.add_route('/walikelas', walikelas_api)
app.add_route('/walikelas/{id:int}', walikelas_detail_api)

app.add_route('/peminjaman', peminjaman_api)
app.add_route('/peminjaman/{id:int}', peminjaman_detail_api)

app.add_route('/jenis-semester', jenis_semester_api)
app.add_route('/jenis-semester/{id:int}', jenis_semester_api)

app.add_route('/mapel', mapel_api)
app.add_route('/mapel/{id:int}', mapel_api)

app.add_route('/semester', semester_api)
app.add_route('/semester/{id:int}', semester_api)

app.add_route('/raport', raport_api)
app.add_route('/raport/{id:int}', raport_api)

app.add_route("/jadwal", jadwal_api)
app.add_route("/jadwal/{id:int}", jadwal_api)
app.add_route("/jadwal/dropdown", jadwal_dropdown_api)

app.add_route("/pegawai", PegawaiResource())
app.add_route("/pegawai/{id:int}", PegawaiResource())

app.add_route("/distribusi-jam", DistribusiJamResource())
app.add_route("/riwayat", RiwayatMengajarResource())


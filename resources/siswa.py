import falcon
import traceback
from pony.orm import db_session, select
from models.schema import Siswa, Kelas, Jurusan, TahunAjaran
from datetime import datetime


# =========================
# SISWA LIST + CREATE
# =========================
class SiswaResource:

    @db_session
    def on_get(self, req, resp):
        search = req.get_param("search")
        kelas = req.get_param("kelas")

        query = select(s for s in Siswa)

        if search:
            keyword = search.lower()

            query = select(
                s for s in Siswa
                if keyword in (s.nama or "").lower()
                or keyword in (s.nis or "").lower()
            )

        if kelas:
            query = select(
                s for s in query
                if s.kelas == kelas
            )

        data = []

        for s in query:
            data.append({
                "id": s.id,
                "nis": s.nis,
                "nisn": s.nisn,
                "nama": s.nama,
                "tempat_lahir": s.tempat_lahir,

                "tanggal_lahir":
                    s.tanggal_lahir.isoformat()
                    if s.tanggal_lahir else None,

                "jenis_kelamin": s.jenis_kelamin,
                "agama": s.agama,
                "golongan_darah": s.golongan_darah,
                "alamat": s.alamat,
                "status": s.status,
                "kelas": s.kelas,
                "jurusan": s.jurusan,
                "tahun_ajaran": s.tahun_ajaran,
                "tahun_masuk": s.tahun_masuk,
                "hp": s.hp,
                "sekolah_asal": s.sekolah_asal,
                "ayah": s.ayah,
                "ibu": s.ibu,
                "wali": s.wali,
                "pekerjaan_ayah": s.pekerjaan_ayah,
                "pekerjaan_ibu": s.pekerjaan_ibu,
                "hp_ayah": s.hp_ayah,
                "hp_ibu": s.hp_ibu,
                "hp_wali": s.hp_wali,
                "hubungan_wali": s.hubungan_wali
            })

        resp.media = {
            "status": True,
            "data": data
        }

    @db_session
    def on_post(self, req, resp):
        body = req.media

        tanggal = None

        if body.get("tanggal_lahir"):
            try:
                tanggal = datetime.strptime(
                    body["tanggal_lahir"],
                    "%Y-%m-%d"
                ).date()

            except Exception:
                tanggal = None

        siswa = Siswa(
            nis=body.get("nis"),
            nisn=body.get("nisn"),
            nama=body.get("nama"),
            tempat_lahir=body.get("tempat_lahir"),
            tanggal_lahir=tanggal,
            jenis_kelamin=body.get("jenis_kelamin"),
            alamat=body.get("alamat"),
            agama=body.get("agama"),
            golongan_darah=body.get("golongan_darah"),
            status=body.get("status"),
            tahun_ajaran=body.get("tahun_ajaran"),
            tahun_masuk=body.get("tahun_masuk"),
            kelas=body.get("kelas"),
            jurusan=body.get("jurusan"),
            hp=body.get("hp"),
            sekolah_asal=body.get("sekolah_asal"),
            ayah=body.get("ayah"),
            ibu=body.get("ibu"),
            wali=body.get("wali"),
            pekerjaan_ayah=body.get("pekerjaan_ayah"),
            pekerjaan_ibu=body.get("pekerjaan_ibu"),
            hp_ayah=body.get("hp_ayah"),
            hp_ibu=body.get("hp_ibu"),
            hp_wali=body.get("hp_wali"),
            hubungan_wali=body.get("hubungan_wali")
        )

        resp.media = {
            "status": True,
            "message": "Data siswa berhasil ditambahkan",
            "id": siswa.id
        }


# =========================
# DROPDOWN DATA
# =========================
class SiswaDropdownResource:

    @db_session
    def on_get(self, req, resp):
        resp.media = {
            "status": True,
            "data": {
                "kelas": [
                    {
                        "id": k.id,
                        "nama": k.nama_kelas
                    }
                    for k in select(k for k in Kelas)
                ],

                "jurusan": [
                    {
                        "id": j.id,
                        "nama": j.nama_jurusan
                    }
                    for j in select(j for j in Jurusan)
                ],

                "tahun_ajaran": [
                    {
                        "id": t.id,
                        "nama": t.tahun_ajaran
                    }
                    for t in select(t for t in TahunAjaran)
                ]
            }
        }


# =========================
# DETAIL + UPDATE + DELETE
# =========================
class DetailSiswaResource:

    @db_session
    def on_get(self, req, resp, id):
        siswa = Siswa.get(id=id)

        if not siswa:
            raise falcon.HTTPNotFound()

        resp.media = {
            "status": True,

            "data":
                siswa.to_dict()
                if hasattr(siswa, "to_dict")
                else {

                "id": siswa.id,
                "nis": siswa.nis,
                "nisn": siswa.nisn,
                "nama": siswa.nama,
                "tempat_lahir": siswa.tempat_lahir,

                "tanggal_lahir":
                    siswa.tanggal_lahir.isoformat()
                    if siswa.tanggal_lahir else None,

                "jenis_kelamin": siswa.jenis_kelamin,
                "agama": siswa.agama,
                "golongan_darah": siswa.golongan_darah,
                "alamat": siswa.alamat,
                "status": siswa.status,
                "kelas": siswa.kelas,
                "jurusan": siswa.jurusan,
                "tahun_ajaran": siswa.tahun_ajaran,
                "tahun_masuk": siswa.tahun_masuk,
                "hp": siswa.hp,
                "sekolah_asal": siswa.sekolah_asal,
                "ayah": siswa.ayah,
                "ibu": siswa.ibu,
                "wali": siswa.wali,
                "pekerjaan_ayah": siswa.pekerjaan_ayah,
                "pekerjaan_ibu": siswa.pekerjaan_ibu,
                "hp_ayah": siswa.hp_ayah,
                "hp_ibu": siswa.hp_ibu,
                "hp_wali": siswa.hp_wali,
                "hubungan_wali": siswa.hubungan_wali
            }
        }

    @db_session
    def on_put(self, req, resp, id):
        try:
            data = req.media

            siswa = Siswa.get(id=id)

            if not siswa:
                raise falcon.HTTPNotFound()

            # =========================
            # PARSE TANGGAL
            # =========================
            tgl_final = siswa.tanggal_lahir

            if data.get("tanggal_lahir"):
                try:
                    tgl_final = datetime.strptime(
                        data["tanggal_lahir"],
                        "%Y-%m-%d"
                    ).date()

                except Exception:
                    tgl_final = siswa.tanggal_lahir

            # =========================
            # UPDATE FIELD
            # =========================
            update_fields = {
                "nis": data.get("nis", siswa.nis),

                "nisn":
                    data.get("nisn", siswa.nisn),

                "nama":
                    data.get("nama", siswa.nama),

                "tempat_lahir":
                    data.get(
                        "tempat_lahir",
                        siswa.tempat_lahir
                    ),

                "tanggal_lahir":
                    tgl_final,

                "jenis_kelamin":
                    data.get(
                        "jenis_kelamin",
                        siswa.jenis_kelamin
                    ),

                "alamat":
                    data.get(
                        "alamat",
                        siswa.alamat
                    ),

                "agama":
                    data.get(
                        "agama",
                        siswa.agama
                    ),

                "golongan_darah":
                    data.get(
                        "golongan_darah",
                        siswa.golongan_darah
                    ),

                "status":
                    data.get(
                        "status",
                        siswa.status
                    ),

                "tahun_ajaran":
                    data.get(
                        "tahun_ajaran",
                        siswa.tahun_ajaran
                    ),

                "tahun_masuk":
                    data.get(
                        "tahun_masuk",
                        siswa.tahun_masuk
                    ),

                "kelas":
                    data.get(
                        "kelas",
                        siswa.kelas
                    ),

                "jurusan":
                    data.get(
                        "jurusan",
                        siswa.jurusan
                    ),

                "hp":
                    data.get(
                        "hp",
                        siswa.hp
                    ),

                "sekolah_asal":
                    data.get(
                        "sekolah_asal",
                        siswa.sekolah_asal
                    ),

                "ayah":
                    data.get(
                        "ayah",
                        siswa.ayah
                    ),

                "ibu":
                    data.get(
                        "ibu",
                        siswa.ibu
                    ),

                "wali":
                    data.get(
                        "wali",
                        siswa.wali
                    ),

                "pekerjaan_ayah":
                    data.get(
                        "pekerjaan_ayah",
                        siswa.pekerjaan_ayah
                    ),

                "pekerjaan_ibu":
                    data.get(
                        "pekerjaan_ibu",
                        siswa.pekerjaan_ibu
                    ),

                "hp_ayah":
                    data.get(
                        "hp_ayah",
                        siswa.hp_ayah
                    ),

                "hp_ibu":
                    data.get(
                        "hp_ibu",
                        siswa.hp_ibu
                    ),

                "hp_wali":
                    data.get(
                        "hp_wali",
                        siswa.hp_wali
                    ),

                "hubungan_wali":
                    data.get(
                        "hubungan_wali",
                        siswa.hubungan_wali
                    )
            }

            siswa.set(**update_fields)

            resp.media = {
                "status": True,
                "message": "Data berhasil diupdate"
            }

        except Exception as e:
            print("ERROR:", e)
            print(traceback.format_exc())

            resp.status = falcon.HTTP_400

            resp.media = {
                "status": False,
                "message": str(e)
            }

    @db_session
    def on_delete(self, req, resp, id):
        siswa = Siswa.get(id=id)

        if not siswa:
            raise falcon.HTTPNotFound()

        siswa.delete()

        resp.media = {
            "status": True,
            "message": "Data siswa berhasil dihapus"
        }
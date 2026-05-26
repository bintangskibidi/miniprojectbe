import falcon
from pony.orm import db_session, commit
import pony.orm as pny

# Pastikan model di models/schema.py Anda memiliki field yang sesuai dengan mapping ini
from models.schema import KriteriaKehadiran, SettingGajiKehadiran


# ==========================================
# 1. RESOURCE KRITERIA KEHADIRAN
# ==========================================
class KriteriaKehadiranResource:

    @db_session
    def on_get(self, req, resp):
        try:
            query = KriteriaKehadiran.select()

            # Disesuaikan 100% dengan state kriteria FE: id, nama, kategori, potongan, tunjangan, range
            data = [
                {
                    "id": k.id,
                    "nama": k.nama,
                    "kategori": k.kategori,
                    "potongan": bool(k.potongan),
                    "tunjangan": bool(k.tunjangan),
                    "range": bool(k.range)
                }
                for k in query
            ]

            resp.media = {
                "status": True,
                "data": data
            }
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": False, "message": str(e)}

    @db_session
    def on_post(self, req, resp):
        try:
            body = req.media

            # Validasi input sesuai form SweetAlert FE (nama & kategori wajib)
            required_fields = ["nama", "kategori"]
            if not body or not all(body.get(field) for field in required_fields):
                resp.status = falcon.HTTP_400
                resp.media = {
                    "status": False,
                    "message": "Semua field (nama, kategori) wajib diisi!"
                }
                return

            # Default nilai boolean di set ke False seperti inisialisasi state di FE (+ Tambah Kriteria)
            baru = KriteriaKehadiran(
                nama=body["nama"],
                kategori=body["kategori"],
                potongan=body.get("potongan", False),
                tunjangan=body.get("tunjangan", False),
                range=body.get("range", False)
            )

            commit()

            resp.status = falcon.HTTP_201
            resp.media = {
                "status": True,
                "message": "Data kriteria berhasil ditambahkan",
                "id": baru.id
            }

        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": False, "message": str(e)}


class DetailKriteriaKehadiranResource:

    @db_session
    def on_put(self, req, resp, id):
        try:
            body = req.media
            item = KriteriaKehadiran.get(id=int(id))

            if not item:
                resp.status = falcon.HTTP_404
                resp.media = {"status": False, "message": "Data kriteria tidak ditemukan"}
                return

            # Update kriteria sesuai dengan form Edit Kriteria di FE
            item.set(
                nama=body.get("nama", item.nama),
                kategori=body.get("kategori", item.kategori),
                potongan=body.get("potongan", item.potongan),
                tunjangan=body.get("tunjangan", item.tunjangan),
                range=body.get("range", item.range)
            )

            commit()

            resp.media = {
                "status": True,
                "message": "Data kriteria berhasil diupdate"
            }
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": False, "message": str(e)}

    @db_session
    def on_delete(self, req, resp, id):
        try:
            item = KriteriaKehadiran.get(id=int(id))

            if not item:
                resp.status = falcon.HTTP_404
                resp.media = {"status": False, "message": "Data kriteria tidak ditemukan"}
                return

            item.delete()
            commit()

            resp.media = {
                "status": True,
                "message": "Data kriteria berhasil dihapus"
            }
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": False, "message": str(e)}


# ==========================================
# 2. RESOURCE SETTING GAJI KEHADIRAN
# ==========================================
class SettingGajiKehadiranResource:

    @db_session
    def on_get(self, req, resp):
        try:
            query = SettingGajiKehadiran.select()

            # Disesuaikan 100% dengan state settingGaji FE: id, kriteria, durasi, jenis, satuan, nominal, keterangan
            data = [
                {
                    "id": s.id,
                    "kriteria": s.kriteria,
                    "durasi": s.durasi,
                    "jenis": s.jenis,
                    "satuan": s.satuan,
                    "nominal": s.nominal,
                    "keterangan": s.keterangan if s.keterangan else ""
                }
                for s in query
            ]

            resp.media = {
                "status": True,
                "data": data
            }
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": False, "message": str(e)}

    @db_session
    def on_post(self, req, resp):
        try:
            body = req.media

            # Validasi input form Tambah Setting Gaji di FE (Semua field wajib kecuali keterangan)
            required_fields = ["kriteria", "durasi", "jenis", "satuan", "nominal"]
            if not body or not all(body.get(field) for field in required_fields):
                resp.status = falcon.HTTP_400
                resp.media = {
                    "status": False,
                    "message": "Semua field (kriteria, durasi, jenis, satuan, nominal) wajib diisi!"
                }
                return

            baru = SettingGajiKehadiran(
                kriteria=body["kriteria"],
                durasi=body["durasi"],
                jenis=body["jenis"],
                satuan=body["satuan"],
                nominal=body["nominal"],
                keterangan=body.get("keterangan", "")
            )

            commit()

            resp.status = falcon.HTTP_201
            resp.media = {
                "status": True,
                "message": "Data setting gaji berhasil ditambahkan",
                "id": baru.id
            }
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": False, "message": str(e)}


class DetailSettingGajiKehadiranResource:

    @db_session
    def on_put(self, req, resp, id):
        try:
            body = req.media
            item = SettingGajiKehadiran.get(id=int(id))

            if not item:
                resp.status = falcon.HTTP_404
                resp.media = {"status": False, "message": "Data setting gaji tidak ditemukan"}
                return

            # Update sesuai field form Edit Setting di FE
            item.set(
                kriteria=body.get("kriteria", item.kriteria),
                durasi=body.get("durasi", item.durasi),
                jenis=body.get("jenis", item.jenis),
                satuan=body.get("satuan", item.satuan),
                nominal=body.get("nominal", item.nominal),
                keterangan=body.get("keterangan", item.keterangan)
            )

            commit()

            resp.media = {
                "status": True,
                "message": "Data setting gaji berhasil diupdate"
            }
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": False, "message": str(e)}

    @db_session
    def on_delete(self, req, resp, id):
        try:
            item = SettingGajiKehadiran.get(id=int(id))

            if not item:
                resp.status = falcon.HTTP_404
                resp.media = {"status": False, "message": "Data setting gaji tidak ditemukan"}
                return

            item.delete()
            commit()

            resp.media = {
                "status": True,
                "message": "Data setting gaji berhasil dihapus"
            }
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": False, "message": str(e)}
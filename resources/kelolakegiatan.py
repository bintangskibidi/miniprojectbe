import falcon
from pony.orm import db_session
import pony.orm as pny
from models.schema import KelolaKegiatan  # Memastikan menggunakan model KelolaKegiatan


class KelolaKegiatanResource:

    @db_session
    def on_get(self, req, resp):
        # Mengambil semua data kegiatan dari database
        query = KelolaKegiatan.select()

        # Disesuaikan 100% dengan FE: id, nama, jenis, mulai, selesai, lokasi, penanggungjawab, status
        data = [
            {
                "id": k.id,
                "nama": k.nama,
                "jenis": k.jenis,
                "mulai": str(k.mulai) if k.mulai else None,
                "selesai": str(k.selesai) if k.selesai else None,
                "lokasi": k.lokasi,
                "penanggungjawab": k.penanggungjawab,
                "status": k.status if k.status else "Aktif"
            }
            for k in query
        ]

        resp.media = {
            "status": True,
            "data": data
        }

    @db_session
    def on_post(self, req, resp):
        try:
            body = req.media

            # Validasi input sesuai kebutuhan FE (Semua field wajib diisi kecuali status yang memiliki default)
            required_fields = ["nama", "jenis", "mulai", "selesai", "lokasi", "penanggungjawab"]
            if not body or not all(body.get(field) for field in required_fields):
                resp.status = falcon.HTTP_400
                resp.media = {
                    "status": False,
                    "message": "Semua field (nama, jenis, mulai, selesai, lokasi, penanggungjawab) wajib diisi!"
                }
                return

            # Mapping field disesuaikan 100% dengan state form Frontend
            baru = KelolaKegiatan(
                nama=body["nama"],
                jenis=body["jenis"],
                mulai=body["mulai"],
                selesai=body["selesai"],
                lokasi=body["lokasi"],
                penanggungjawab=body["penanggungjawab"],
                status=body.get("status", "Aktif")
            )

            # Flush Pony ORM agar ID baru langsung tergenerasi
            pny.commit()

            resp.status = falcon.HTTP_201
            resp.media = {
                "status": True,
                "message": "Data kegiatan berhasil ditambahkan",
                "id": baru.id
            }

        except Exception as e:
            print("ERROR POST KEGIATAN:", e)
            resp.status = falcon.HTTP_500
            resp.media = {
                "status": False,
                "message": str(e)
            }


class DetailKelolaKegiatanResource:

    @db_session
    def on_get(self, req, resp, id):
        item = KelolaKegiatan.get(id=int(id))

        if not item:
            resp.status = falcon.HTTP_404
            resp.media = {"status": False, "message": "Data kegiatan tidak ditemukan"}
            return

        resp.media = {
            "status": True,
            "data": {
                "id": item.id,
                "nama": item.nama,
                "jenis": item.jenis,
                "mulai": str(item.mulai) if item.mulai else None,
                "selesai": str(item.selesai) if item.selesai else None,
                "lokasi": item.lokasi,
                "penanggungjawab": item.penanggungjawab,
                "status": item.status
            }
        }

    @db_session
    def on_put(self, req, resp, id):
        try:
            body = req.media
            item = KelolaKegiatan.get(id=int(id))

            if not item:
                resp.status = falcon.HTTP_404
                resp.media = {"status": False, "message": "Data kegiatan tidak ditemukan"}
                return

            # Update field disesuaikan dengan skema Form FE saat Edit Data
            item.set(
                nama=body.get("nama", item.nama),
                jenis=body.get("jenis", item.jenis),
                mulai=body.get("mulai", item.mulai),
                selesai=body.get("selesai", item.selesai),
                lokasi=body.get("lokasi", item.lokasi),
                penanggungjawab=body.get("penanggungjawab", item.penanggungjawab),
                status=body.get("status", item.status)
            )

            pny.commit()

            resp.media = {
                "status": True,
                "message": "Data berhasil diupdate"
            }

        except Exception as e:
            print("ERROR PUT KEGIATAN:", e)
            resp.status = falcon.HTTP_500
            resp.media = {
                "status": False,
                "message": str(e)
            }

    @db_session
    def on_delete(self, req, resp, id):
        item = KelolaKegiatan.get(id=int(id))

        if not item:
            resp.status = falcon.HTTP_404
            resp.media = {"status": False, "message": "Data kegiatan tidak ditemukan"}
            return

        item.delete()
        pny.commit()

        resp.media = {
            "status": True,
            "message": "Data berhasil dihapus"
        }
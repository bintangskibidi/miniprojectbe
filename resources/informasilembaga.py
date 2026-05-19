import falcon
from pony.orm import db_session
from models.schema import InformasiLembaga


class InformasiLembagaResource:

    @db_session
    def on_get(self, req, resp):
        # Mengambil semua data dari database
        query = InformasiLembaga.select()

        # Disesuaikan dengan FE: id, judul, isi, tanggal
        data = [
            {
                "id": w.id,
                "judul": w.judul,
                "isi": w.isi,
                "tanggal": str(w.tanggal) if w.tanggal else None
            }
            for w in query
        ]

        resp.media = {
            "status": True,
            "data": data
        }

    @db_session
    def on_post(self, req, resp):
        try:
            body = req.media

            # Validasi input sesuai kebutuhan FE (judul dan isi wajib ada)
            if not body or not body.get("judul") or not body.get("isi"):
                resp.status = falcon.HTTP_400
                resp.media = {
                    "status": False,
                    "message": "Judul dan Isi wajib diisi"
                }
                return

            # Mapping field disesuaikan 100% dengan FE
            baru = InformasiLembaga(
                judul=body["judul"],
                isi=body["isi"],
                tanggal=body.get("tanggal", None)
            )

            # Flush Pony ORM agar ID baru langsung tergenerasi
            import pony.orm as pny
            pny.commit()

            resp.status = falcon.HTTP_201
            resp.media = {
                "status": True,
                "message": "Data berhasil ditambahkan",
                "id": baru.id
            }

        except Exception as e:
            print("ERROR POST:", e)
            resp.status = falcon.HTTP_500
            resp.media = {
                "status": False,
                "message": str(e)
            }


class DetailInformasiLembagaResource:

    @db_session
    def on_get(self, req, resp, id):  # Perbaikan: Menambahkan parameter id
        item = InformasiLembaga.get(id=int(id))

        if not item:
            resp.status = falcon.HTTP_404
            resp.media = {"status": False, "message": "Data tidak ditemukan"}
            return

        resp.media = {
            "status": True,
            "data": {
                "id": item.id,
                "judul": item.judul,
                "isi": item.isi,
                "tanggal": str(item.tanggal) if item.tanggal else None
            }
        }

    @db_session
    def on_put(self, req, resp, id):
        body = req.media
        item = InformasiLembaga.get(id=int(id))

        if not item:
            resp.status = falcon.HTTP_404
            resp.media = {"status": False, "message": "Data tidak ditemukan"}
            return

        # Update field disesuaikan dengan skema FE
        item.set(
            judul=body.get("judul", item.judul),
            isi=body.get("isi", item.isi),
            tanggal=body.get("tanggal", item.tanggal)
        )

        resp.media = {
            "status": True,
            "message": "Data berhasil diupdate"
        }

    @db_session
    def on_delete(self, req, resp, id):
        item = InformasiLembaga.get(id=int(id))

        if not item:
            resp.status = falcon.HTTP_404
            resp.media = {"status": False, "message": "Data tidak ditemukan"}
            return

        item.delete()

        resp.media = {
            "status": True,
            "message": "Data berhasil dihapus"
        }
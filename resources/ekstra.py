import falcon
from pony.orm import db_session
from models.schema import EkstraKulikuler


class EkstraKulikulerResource:

    @db_session
    def on_get(self, req, resp):
        query = EkstraKulikuler.select()

        data = [
            {
                "id": w.id,
                "nama": w.nama_kelas,
                "pembina": w.nama_pegawai,
                "jadwal": w.jadwal,
                "tanggal": w.tanggal,
                "keterangan": w.keterangan
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

            if not body or not body.get("nama"):
                resp.status = falcon.HTTP_400
                resp.media = {
                    "status": False,
                    "message": "Nama wajib diisi"
                }
                return

            baru = EkstraKulikuler(
                nama_kelas=body["nama"],
                nama_pegawai=body.get("pembina", ""),
                jadwal=body.get("jadwal", ""),
                tanggal=body.get("tanggal", None),  # biar aman date/null
                keterangan=body.get("keterangan", "")
            )

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


class DetailekstrakurikulerResource:

    @db_session
    def on_get(self, req, resp):
        item = EkstraKulikuler.get(id=int(id))

        if not item:
            resp.status = falcon.HTTP_404
            resp.media = {"status": False, "message": "Data tidak ditemukan"}
            return

        resp.media = {
            "status": True,
            "data": {
                "id": item.id,
                "nama": item.nama_kelas,
                "pembina": item.nama_pegawai,
                "jadwal": item.jadwal,
                "tanggal": item.tanggal,
                "keterangan": item.keterangan
            }
        }

    @db_session
    def on_put(self, req, resp, id):
        body = req.media
        item = EkstraKulikuler.get(id=int(id))

        if not item:
            resp.status = falcon.HTTP_404
            resp.media = {"status": False, "message": "Data tidak ditemukan"}
            return

        item.set(
            nama_kelas=body.get("nama", item.nama_kelas),
            nama_pegawai=body.get("pembina", item.nama_pegawai),
            jadwal=body.get("jadwal", item.jadwal),
            tanggal=body.get("tanggal", item.tanggal),
            keterangan=body.get("keterangan", item.keterangan)
        )

        resp.media = {
            "status": True,
            "message": "Data berhasil diupdate"
        }

    @db_session
    def on_delete(self, req, resp, id):  # Tambahkan parameter id di sini
        item = EkstraKulikuler.get(id=int(id))

        if not item:
            resp.status = falcon.HTTP_404
            resp.media = {"status": False, "message": "Data tidak ditemukan"}
            return

        item.delete()

        resp.media = {
            "status": True,
            "message": "Data berhasil dihapus"
        }
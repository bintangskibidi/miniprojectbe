import falcon
from pony.orm import db_session, select
from models.schema import AspekPenilaian


class AspekPenilaianResource:
    @db_session
    def on_get(self, req, resp, id=None):
        if id:
            try:
                aspek = AspekPenilaian[id]
                resp.media = {
                    "status": True,
                    "data": aspek.to_dict()
                }
            except Exception:
                resp.status = falcon.HTTP_404
                resp.media = {
                    "status": False,
                    "message": "Data aspek penilaian tidak ditemukan"
                }
        else:
            data = [a.to_dict() for a in select(a for a in AspekPenilaian)]
            resp.media = {
                "status": True,
                "data": data
            }

    @db_session
    def on_post(self, req, resp):
        data = req.media
        try:
            aspek = AspekPenilaian(
                kode_aspek=data['kode_aspek'],
                nama_aspek=data['nama_aspek']
            )
            resp.media = {
                "status": True,
                "message": "Aspek penilaian berhasil ditambahkan",
                "data": aspek.to_dict()
            }
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {
                "status": False,
                "message": str(e)
            }

    @db_session
    def on_put(self, req, resp, id):
        data = req.media
        try:
            aspek = AspekPenilaian[id]
            aspek.kode_aspek = data.get('kode_aspek', aspek.kode_aspek)
            aspek.nama_aspek = data.get('nama_aspek', aspek.nama_aspek)

            resp.media = {
                "status": True,
                "message": "Aspek penilaian berhasil diperbarui",
                "data": aspek.to_dict()
            }
        except Exception:
            resp.status = falcon.HTTP_404
            resp.media = {
                "status": False,
                "message": "Data aspek penilaian tidak ditemukan"
            }

    @db_session
    def on_delete(self, req, resp, id):
        try:
            aspek = AspekPenilaian[id]
            aspek.delete()
            resp.media = {
                "status": True,
                "message": "Aspek penilaian berhasil dihapus"
            }
        except Exception:
            resp.status = falcon.HTTP_404
            resp.media = {
                "status": False,
                "message": "Data aspek penilaian tidak ditemukan"
            }

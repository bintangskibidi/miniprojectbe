import falcon
from pony.orm import db_session, select
from models.schema import Mapel


class MapelResource:

    @db_session
    def on_get(self, req, resp, id=None):
        if id:
            try:
                mapel = Mapel[id]
                resp.media = {
                    "status": True,
                    "data": mapel.to_dict()
                }
            except Exception:
                resp.status = falcon.HTTP_404
                resp.media = {
                    "status": False,
                    "message": "Mata pelajaran tidak ditemukan"
                }
        else:
            data = [m.to_dict() for m in select(m for m in Mapel)]
            resp.media = {
                "status": True,
                "data": data
            }

    @db_session
    def on_post(self, req, resp):
        data = req.media
        try:
            mapel = Mapel(
                nama=data["nama"]
            )
            resp.media = {
                "status": True,
                "message": "Mata pelajaran berhasil ditambahkan",
                "data": mapel.to_dict()
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
            mapel = Mapel[id]
            mapel.nama = data.get("nama", mapel.nama)

            resp.media = {
                "status": True,
                "message": "Mata pelajaran berhasil diupdate",
                "data": mapel.to_dict()
            }
        except Exception:
            resp.status = falcon.HTTP_404
            resp.media = {
                "status": False,
                "message": "Mata pelajaran tidak ditemukan"
            }

    @db_session
    def on_delete(self, req, resp, id):
        try:
            mapel = Mapel[id]
            mapel.delete()

            resp.media = {
                "status": True,
                "message": "Mata pelajaran berhasil dihapus"
            }
        except Exception:
            resp.status = falcon.HTTP_404
            resp.media = {
                "status": False,
                "message": "Mata pelajaran tidak ditemukan"
            }
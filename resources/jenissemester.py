import falcon
from pony.orm import db_session, select
from models.schema import JenisSemester


class JenisSemesterResource:
    @db_session
    def on_get(self, req, resp, id=None):
        if id:
            try:
                jenis_semester = JenisSemester[id]
                resp.media = {
                    "status": True,
                    "data": jenis_semester.to_dict()
                }
            except Exception:
                resp.status = falcon.HTTP_404
                resp.media = {
                    "status": False,
                    "message": "Jenis semester tidak ditemukan"
                }
        else:
            data = [js.to_dict() for js in select(js for js in JenisSemester)]
            resp.media = {
                "status": True,
                "data": data
            }

    @db_session
    def on_post(self, req, resp):
        data = req.media
        try:
            jenis_semester = JenisSemester(
                nama=data["nama"]
            )
            resp.media = {
                "status": True,
                "message": "Jenis semester berhasil ditambahkan",
                "data": jenis_semester.to_dict()
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
            jenis_semester = JenisSemester[id]
            jenis_semester.nama = data.get("nama", jenis_semester.nama)

            resp.media = {
                "status": True,
                "message": "Jenis semester berhasil diupdate",
                "data": jenis_semester.to_dict()
            }
        except Exception:
            resp.status = falcon.HTTP_404
            resp.media = {
                "status": False,
                "message": "Jenis semester tidak ditemukan"
            }

    @db_session
    def on_delete(self, req, resp, id):
        try:
            jenis_semester = JenisSemester[id]
            jenis_semester.delete()

            resp.media = {
                "status": True,
                "message": "Jenis semester berhasil dihapus"
            }
        except Exception:
            resp.status = falcon.HTTP_404
            resp.media = {
                "status": False,
                "message": "Jenis semester tidak ditemukan"
            }
import falcon
from pony.orm import db_session, select
from models.schema import TahunAjaran


class TahunAjaranResource:
    @db_session
    def on_get(self, req, resp, id=None):
        if id:
            try:
                ta = TahunAjaran[id]
                resp.media = {"status": True, "data": ta.to_dict()}
            except Exception:
                resp.status = falcon.HTTP_404
                resp.media = {
                    "status": False,
                    "message": "Tahun ajaran tidak ditemukan"
                }
        else:
            data = [ta.to_dict() for ta in select(ta for ta in TahunAjaran)]
            resp.media = {"status": True, "data": data}

    @db_session
    def on_post(self, req, resp):
        data = req.media
        try:
            tahun_ajaran = TahunAjaran(
                tahun_ajaran=data['tahun_ajaran'],
                tahun=data['tahun'],
                status=data.get('status', True)
            )
            resp.media = {
                "status": True,
                "message": "Tahun ajaran berhasil ditambahkan",
                "data": tahun_ajaran.to_dict()
            }
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": False, "message": str(e)}

    @db_session
    def on_put(self, req, resp, id):
        data = req.media
        try:
            ta = TahunAjaran[id]
            ta.tahun_ajaran = data.get('tahun_ajaran', ta.tahun_ajaran)
            ta.tahun = data.get('tahun', ta.tahun)
            if 'status' in data:
                ta.status = data['status']

            resp.media = {
                "status": True,
                "message": "Tahun ajaran berhasil diupdate",
                "data": ta.to_dict()
            }
        except Exception:
            resp.status = falcon.HTTP_404
            resp.media = {
                "status": False,
                "message": "Tahun ajaran tidak ditemukan"
            }

    @db_session
    def on_patch(self, req, resp, id):
        try:
            ta = TahunAjaran[id]
            ta.status = not ta.status
            resp.media = {
                "status": True,
                "message": f"Tahun ajaran berhasil {'diaktifkan' if ta.status else 'dinonaktifkan'}",
                "data": ta.to_dict()
            }
        except Exception:
            resp.status = falcon.HTTP_404
            resp.media = {
                "status": False,
                "message": "Tahun ajaran tidak ditemukan"
            }

    @db_session
    def on_delete(self, req, resp, id):
        try:
            ta = TahunAjaran[id]
            ta.delete()
            resp.media = {
                "status": True,
                "message": "Tahun ajaran berhasil dihapus"
            }
        except Exception:
            resp.status = falcon.HTTP_404
            resp.media = {
                "status": False,
                "message": "Tahun ajaran tidak ditemukan"
            }

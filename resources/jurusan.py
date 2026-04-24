import falcon
from pony.orm import db_session, select
from models.schema import Jurusan 

class JurusanResource:
    @db_session
    def on_get(self, req, resp, id=None):
        if id:
            try:
                j = Jurusan[id]
                resp.media = {"status": True, "data": j.to_dict()}
            except:
                resp.status = falcon.HTTP_404
                resp.media = {"status": False, "message": "Jurusan tidak ditemukan"}
        else:
            # Ambil semua data untuk ditampilkan di tabel
            data = [j.to_dict() for j in select(j for j in Jurusan)]
            resp.media = {"status": True, "data": data}

    @db_session
    def on_post(self, req, resp):
        data = req.media
        try:
            Jurusan(kode_jurusan=data['kode_jurusan'], nama_jurusan=data['nama_jurusan'])
            resp.media = {"status": True, "message": "Jurusan berhasil ditambah"}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": False, "message": str(e)}

    @db_session
    def on_put(self, req, resp, id):
        data = req.media
        try:
            j = Jurusan[id]
            j.set(**data)
            resp.media = {"status": True, "message": "Jurusan berhasil diupdate"}
        except:
            resp.status = falcon.HTTP_404

    @db_session
    def on_delete(self, req, resp, id):
        try:
            j = Jurusan[id]
            j.delete()
            resp.media = {"status": True, "message": "Jurusan berhasil dihapus"}
        except:
            resp.status = falcon.HTTP_404
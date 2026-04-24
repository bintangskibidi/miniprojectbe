import falcon
from pony.orm import db_session, select
from models.schema import Kelas

class KelasResource:
    @db_session
    def on_get(self, req, resp, id=None):
        if id:
            # Ambil detail satu kelas
            try:
                k = Kelas[id]
                resp.media = {"status": True, "data": k.to_dict()}
            except:
                resp.status = falcon.HTTP_404
                resp.media = {"status": False, "message": "Data tidak ditemukan"}
        else:
            # Ambil semua daftar kelas
            data = [k.to_dict() for k in select(k for k in Kelas)]
            resp.media = {"status": True, "data": data}

    @db_session
    def on_post(self, req, resp):
        # Tambah Kelas Baru
        data = req.media
        try:
            Kelas(kode_kelas=data['kode_kelas'], nama_kelas=data['nama_kelas'])
            resp.media = {"status": True, "message": "Kelas berhasil ditambah"}
        except Exception as e:
            resp.status = falcon.HTTP_500 # Hindari error 500 tanpa pesan
            resp.media = {"status": False, "message": str(e)}

    @db_session
    def on_put(self, req, resp, id):
        # Update Kelas
        data = req.media
        try:
            k = Kelas[id]
            k.set(**data)
            resp.media = {"status": True, "message": "Data berhasil diubah"}
        except:
            resp.status = falcon.HTTP_404

    @db_session
    def on_delete(self, req, resp, id):
        # Hapus Kelas
        try:
            k = Kelas[id]
            k.delete()
            resp.media = {"status": True, "message": "Data dihapus"}
        except:
            resp.status = falcon.HTTP_404
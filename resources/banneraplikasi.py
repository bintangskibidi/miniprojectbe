import falcon
from pony.orm import db_session, select
from datetime import datetime
# Pastikan path import schema ini sesuai dengan struktur folder project Anda
from models.schema import Banner


class BannerAplikasiResource:

    @db_session
    def on_get(self, req, resp, id=None):
        if id:
            try:
                b = Banner[id]
                resp.media = {"status": True, "data": b.to_dict()}
            except:
                resp.status = falcon.HTTP_404
                resp.media = {"status": False, "message": "Banner tidak ditemukan"}
        else:
            # Ambil semua data banner urut berdasarkan id terbaru (opsional)
            query = select(b for b in Banner).order_by(lambda b: b.id)
            data = [b.to_dict() for b in query]
            resp.media = {"status": True, "data": data}

    @db_session
    def on_post(self, req, resp):
        try:
            data = req.media
            if not data or 'nama' not in data or 'gambar' not in data:
                resp.status = falcon.HTTP_400
                resp.media = {"status": False, "message": "Data nama dan gambar wajib diisi"}
                return

            # Membuat baris Banner baru sesuai properti frontend
            new_banner = Banner(
                nama=data['nama'],
                gambar=data['gambar'],
                tanggal=datetime.now()  # Otomatis generate waktu server saat diupload
            )

            # Flush untuk mendapatkan ID baru dari database
            import pony.orm as pny
            pny.flush()

            resp.status = falcon.HTTP_201
            resp.media = {
                "status": True,
                "message": "Banner berhasil diupload",
                "data": new_banner.to_dict()
            }
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": False, "message": str(e)}

    @db_session
    def on_put(self, req, resp, id):
        try:
            data = req.media
            b = Banner[id]

            # Update data jika dikirim dari frontend
            if 'nama' in data: b.nama = data['nama']
            if 'gambar' in data: b.gambar = data['gambar']

            resp.media = {"status": True, "message": "Banner berhasil diupdate"}
        except:
            resp.status = falcon.HTTP_404
            resp.media = {"status": False, "message": "Banner tidak ditemukan"}

    @db_session
    def on_delete(self, req, resp, id):
        try:
            b = Banner[id]
            b.delete()
            resp.media = {"status": True, "message": "Banner berhasil dihapus"}
        except:
            resp.status = falcon.HTTP_404
            resp.media = {"status": False, "message": "Banner tidak ditemukan atau gagal dihapus"}
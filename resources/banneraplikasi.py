import os
import falcon
from pony.orm import db_session, select
from datetime import datetime
import pony.orm as pny

# Pastikan path import schema ini sesuai dengan struktur folder project Anda
from models.schema import Banner

# Tentukan folder penyimpanan file banner statis di server Anda
UPLOAD_DIR = os.path.join(os.getcwd(), 'static', 'uploads', 'banners')
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR, exist_ok=True)


class BannerAplikasiResource:

    @db_session
    def on_get(self, req, resp, id=None):
        if id:
            try:
                b = Banner[id]
                resp.media = {"status": True, "data": b.to_dict()}
            except Exception:
                resp.status = falcon.HTTP_404
                resp.media = {"status": False, "message": "Banner tidak ditemukan"}
        else:
            # Mengambil data banner diurutkan berdasarkan ID terbaru agar sinkron dengan UI
            query = select(b for b in Banner).order_by(lambda b: pny.desc(b.id))
            data = [b.to_dict() for b in query]
            resp.media = {"status": True, "data": data}


    @db_session
    def on_post(self, req, resp):
        try:
            # Ambil multipart form (Pastikan app.req_options.media_handlers['multipart/form-data'] sudah aktif di main/app.py)
            form = req.get_media()

            file_part = None

            # Falcon multipart memerlukan iterasi atau pengecekan manual pada part form
            for part in form:
                if part.name == "gambar":
                    file_part = part
                    break

            if not file_part:
                resp.status = falcon.HTTP_400
                resp.media = {
                    "status": False,
                    "message": "Berkas gambar wajib diisi"
                }
                return

            # Nama file asli
            original_filename = file_part.filename

            # Nama file unik
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            secure_filename = f"{timestamp}_{original_filename}"

            file_path = os.path.join(UPLOAD_DIR, secure_filename)

            # Simpan file menggunakan part.stream
            with open(file_path, "wb") as output_file:
                output_file.write(file_part.stream.read())  # <-- PERBAIKAN: Gunakan .stream.read() bukan .file.read()

            # URL akses gambar
            web_accessible_path = f"http://localhost:8000/static/uploads/banners/{secure_filename}"

            # Simpan ke database (Sesuaikan format tanggal dengan tipe field di schema.py)
            new_banner = Banner(
                nama=original_filename,
                gambar=web_accessible_path,
                tanggal=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # <-- DIKEMBALIKAN KE STR: Lebih aman jika field database berupa String
            )

            pny.flush()

            resp.status = falcon.HTTP_201
            resp.media = {
                "status": True,
                "message": "Banner berhasil diupload",
                "data": new_banner.to_dict()
            }

        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {
                "status": False,
                "message": f"Terjadi kesalahan: {str(e)}"
            }
    @db_session
    def on_put(self, req, resp, id):
        # Menu PUT/Update tidak dipakai di frontend Anda, namun tetap diselaraskan strukturnya
        try:
            data = req.media or {}
            b = Banner[id]

            if 'nama' in data: b.nama = data['nama']
            if 'gambar' in data: b.gambar = data['gambar']

            resp.media = {"status": True, "message": "Banner berhasil diupdate"}
        except Exception:
            resp.status = falcon.HTTP_404
            resp.media = {"status": False, "message": "Banner tidak ditemukan"}

    @db_session
    def on_delete(self, req, resp, id):
        try:
            b = Banner[id]

            # (Opsional) Menghapus file fisik dari penyimpanan server lokal saat data dihapus
            try:
                filename_only = b.gambar.split('/')[-1]
                target_file = os.path.join(UPLOAD_DIR, filename_only)
                if os.path.exists(target_file):
                    os.remove(target_file)
            except Exception:
                pass  # Abaikan jika file fisik sudah tidak ada

            b.delete()
            resp.media = {"status": True, "message": "Banner berhasil dihapus"}
        except Exception:
            resp.status = falcon.HTTP_404
            resp.media = {"status": False, "message": "Banner tidak ditemukan atau gagal dihapus"}
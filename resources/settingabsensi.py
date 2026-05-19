import falcon
from pony.orm import db_session, select
# Pastikan path import schema ini sesuai dengan struktur folder project Anda
# Di sini kita berasumsi nama Entity-nya adalah AbsensiGPS
from models.schema import AbsensiGPS


class SettingAbsensiResource:

    @db_session
    def on_get(self, req, resp, id=None):
        if id:
            try:
                # Mengambil detail data berdasarkan ID
                b = AbsensiGPS[id]
                resp.media = {"status": True, "data": b.to_dict()}
            except:
                resp.status = falcon.HTTP_404
                resp.media = {"status": False, "message": "Data lokasi absensi tidak ditemukan"}
        else:
            # Ambil semua data lokasi urut berdasarkan id terbaru/terlama
            query = select(b for b in AbsensiGPS).order_by(lambda b: b.id)
            data = [b.to_dict() for b in query]
            resp.media = {"status": True, "data": data}

    @db_session
    def on_post(self, req, resp):
        try:
            data = req.media

            # Validasi kelengkapan data sesuai inputan dari form frontend
            required_fields = ['nama', 'latitude', 'longitude', 'radius', 'masuk', 'selesai']
            if not data or not all(field in data for field in required_fields):
                resp.status = falcon.HTTP_400
                resp.media = {"status": False,
                              "message": "Semua field wajib diisi (nama, latitude, longitude, radius, masuk, selesai)"}
                return

            # Membuat baris AbsensiGPS baru sesuai properti frontend
            new_lokasi = AbsensiGPS(
                nama=data['nama'],
                latitude=str(data['latitude']),
                longitude=str(data['longitude']),
                radius=str(data['radius']),
                masuk=data['masuk'],  # Format "HH:MM"
                selesai=data['selesai']  # Format "HH:MM"
            )

            # Flush untuk mendapatkan ID baru dari database
            import pony.orm as pny
            pny.flush()

            resp.status = falcon.HTTP_201
            resp.media = {
                "status": True,
                "message": "Lokasi absensi berhasil ditambahkan",
                "data": new_lokasi.to_dict()
            }
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": False, "message": str(e)}

    @db_session
    def on_put(self, req, resp, id):
        try:
            data = req.media
            if not data:
                resp.status = falcon.HTTP_400
                resp.media = {"status": False, "message": "Data update tidak boleh kosong"}
                return

            # Ambil baris data berdasarkan ID yang dikirim melalui URL parameter
            b = AbsensiGPS[id]

            # Update data jika dikirim dari frontend (Fleksibel jika hanya kirim sebagian)
            if 'nama' in data: b.nama = data['nama']
            if 'latitude' in data: b.latitude = str(data['latitude'])
            if 'longitude' in data: b.longitude = str(data['longitude'])
            if 'radius' in data: b.radius = str(data['radius'])
            if 'masuk' in data: b.masuk = data['masuk']
            if 'selesai' in data: b.selesai = data['selesai']

            resp.media = {
                "status": True,
                "message": "Lokasi absensi berhasil diupdate",
                "data": b.to_dict()
            }
        except Exception as e:
            resp.status = falcon.HTTP_404
            resp.media = {"status": False, "message": "Lokasi absensi tidak ditemukan atau gagal diupdate"}

    @db_session
    def on_delete(self, req, resp, id):
        try:
            b = AbsensiGPS[id]
            b.delete()
            resp.media = {"status": True, "message": "Lokasi absensi berhasil dihapus"}
        except:
            resp.status = falcon.HTTP_404
            resp.media = {"status": False, "message": "Lokasi absensi tidak ditemukan atau gagal dihapus"}
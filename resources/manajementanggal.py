import falcon
import pony.orm as pny
from pony.orm import db_session
# Silakan sesuaikan import model database di bawah ini dengan lokasi proyek Anda
from models.schema import PeriodeTanggal

class ManajemenTanggalResource:

    @db_session
    def on_get(self, req, resp):
        """
        Mengambil semua daftar tanggal sistem.
        Disesuaikan 100% dengan struktur array FE: [{id, tanggal, status}]
        """
        try:
            # Mengambil data tanggal dan mengurutkannya secara ascending berdasarkan angka tanggal
            query = PeriodeTanggal.select().order_by(lambda p: p.tanggal)

            data = [
                {
                    "id": p.id,
                    "tanggal": p.tanggal,
                    "status": p.status if p.status else "Aktif"
                }
                for p in query
            ]

            resp.status = falcon.HTTP_200
            resp.media = data  # Menghasilkan array langsung untuk kebutuhan setTanggalList() FE

        except Exception as e:
            print("ERROR GET MANAJEMEN TANGGAL:", e)
            resp.status = falcon.HTTP_500
            resp.media = {"status": False, "message": str(e)}

    @db_session
    def on_post(self, req, resp):
        """
        Menambah tanggal baru (1-31).
        Validasi meniru persis preConfirm SweetAlert di Frontend.
        """
        try:
            body = req.media or {}
            tanggal_raw = body.get("tanggal")

            # 1. Validasi: Tanggal wajib diisi
            if tanggal_raw is None or str(tanggal_raw).strip() == "":
                resp.status = falcon.HTTP_400
                resp.media = {
                    "status": False,
                    "message": "Tanggal wajib diisi"
                }
                return

            # Konversi input ke integer
            try:
                tanggal = int(tanggal_raw)
            except ValueError:
                resp.status = falcon.HTTP_400
                resp.media = {
                    "status": False,
                    "message": "Tanggal harus berupa angka"
                }
                return

            # 2. Validasi: Tanggal harus antara 1 - 31
            if tanggal < 1 or tanggal > 31:
                resp.status = falcon.HTTP_400
                resp.media = {
                    "status": False,
                    "message": "Tanggal harus antara 1 - 31"
                }
                return

            # 3. Validasi: Cek apakah tanggal sudah terdaftar (Duplikasi)
            sudah_ada = PeriodeTanggal.get(tanggal=tanggal)
            if sudah_ada:
                resp.status = falcon.HTTP_400
                resp.media = {
                    "status": False,
                    "message": "Tanggal sudah ada"
                }
                return

            # Simpan data baru ke database jika lolos semua validasi
            # Jika FE mengirimkan ID kustom berbasis Date.now(), gunakan body.get("id")
            # Jika database auto-increment, biarkan terisi otomatis.
            baru = PeriodeTanggal(
                id=body.get("id") if "id" in body else None,
                tanggal=tanggal,
                status="Aktif" # Otomatis aktif seperti di FE
            )

            pny.commit()

            resp.status = falcon.HTTP_201
            resp.media = {
                "id": baru.id,
                "tanggal": baru.tanggal,
                "status": baru.status
            }

        except Exception as e:
            print("ERROR POST MANAJEMEN TANGGAL:", e)
            resp.status = falcon.HTTP_500
            resp.media = {"status": False, "message": str(e)}


class DetailTanggalResource:

    @db_session
    def on_get(self, req, resp, id):
        """
        Melihat detail data tanggal spesifik berdasarkan ID
        """
        try:
            item = PeriodeTanggal.get(id=int(id))

            if not item:
                resp.status = falcon.HTTP_404
                resp.media = {
                    "status": False,
                    "message": "Data tanggal tidak ditemukan",
                }
                return

            resp.status = falcon.HTTP_200
            resp.media = {
                "id": item.id,
                "tanggal": item.tanggal,
                "status": item.status,
            }
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": False, "message": str(e)}

    @db_session
    def on_delete(self, req, resp, id):
        """
        Menghapus data tanggal berdasarkan ID.
        Digunakan untuk menangani fungsi hapusTanggal(id) dari FE.
        """
        try:
            item = PeriodeTanggal.get(id=int(id))

            if not item:
                resp.status = falcon.HTTP_404
                resp.media = {
                    "status": False,
                    "message": "Data tanggal tidak ditemukan",
                }
                return

            item.delete()
            pny.commit()

            resp.status = falcon.HTTP_200
            resp.media = {
                "status": True,
                "message": "Tanggal berhasil dihapus"
            }

        except Exception as e:
            print("ERROR DELETE TANGGAL:", e)
            resp.status = falcon.HTTP_500
            resp.media = {"status": False, "message": str(e)}
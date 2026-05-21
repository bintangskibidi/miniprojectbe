import datetime
import falcon
from pony.orm import db_session
import pony.orm as pny
from models.schema import Cuti  # Menggunakan model Cuti asli


class CutiResource:

    @db_session
    def on_get(self, req, resp):
        # Mengambil semua data cuti dari database
        query = Cuti.select()

        # Disesuaikan 100% dengan FE: id, nama, unit, mulai, selesai, alasan, status
        data = [
            {
                "id": c.id,
                "nama": c.nama,
                "unit": c.unit if c.unit else "0",
                "mulai": c.mulai.strftime("%Y-%m-%d") if isinstance(c.mulai,
                                                                    (datetime.date, datetime.datetime)) else str(
                    c.mulai),
                "selesai": c.selesai.strftime("%Y-%m-%d") if isinstance(c.selesai,
                                                                        (datetime.date, datetime.datetime)) else str(
                    c.selesai),
                "alasan": c.alasan,
                "status": c.status if c.status else "Pending"
            }
            for c in query
        ]

        resp.media = data  # Menghasilkan array langsung atau membungkusnya sesuai kebutuhan fetch FE

    @db_session
    def on_post(self, req, resp):
        try:
            body = req.media

            # Validasi input sesuai dengan preConfirm di SweetAlert Frontend (nama, mulai, selesai, alasan)
            required_fields = ["nama", "mulai", "selesai", "alasan"]
            if not body or not all(body.get(field) for field in required_fields):
                resp.status = falcon.HTTP_400
                resp.media = {
                    "status": False,
                    "message": "Semua bidang data harus diisi!"
                }
                return

            # Parsing string ISO date dari FE ("YYYY-MM-DD") ke objek Python datetime/date
            try:
                mulai_dt = datetime.datetime.strptime(body["mulai"], "%Y-%m-%d")
                selesai_dt = datetime.datetime.strptime(body["selesai"], "%Y-%m-%d")
            except ValueError:
                resp.status = falcon.HTTP_400
                resp.media = {
                    "status": False,
                    "message": "Format tanggal mulai atau selesai tidak valid. Gunakan YYYY-MM-DD"
                }
                return

            # Mapping field disesuaikan 100% dengan state data baru di Frontend
            baru = Cuti(
                nama=body["nama"],
                unit=body.get("unit", "0"),  # Default sesuai FE "0"
                mulai=mulai_dt,
                selesai=selesai_dt,
                alasan=body["alasan"],
                status="Pending"  # Pengajuan baru otomatis statusnya "Pending"
            )

            # Flush Pony ORM agar ID baru langsung tergenerasi
            pny.commit()

            resp.status = falcon.HTTP_201
            resp.media = {
                "id": baru.id,
                "nama": baru.nama,
                "unit": baru.unit,
                "mulai": body["mulai"],
                "selesai": body["selesai"],
                "alasan": baru.alasan,
                "status": baru.status
            }

        except Exception as e:
            print("ERROR POST CUTI:", e)
            resp.status = falcon.HTTP_500
            resp.media = {
                "status": False,
                "message": str(e)
            }


class DetailCutiResource:

    @db_session
    def on_get(self, req, resp, id):
        item = Cuti.get(id=int(id))

        if not item:
            resp.status = falcon.HTTP_404
            resp.media = {"status": False, "message": "Data cuti tidak ditemukan"}
            return

        resp.media = {
            "id": item.id,
            "nama": item.nama,
            "unit": item.unit,
            "mulai": item.mulai.strftime("%Y-%m-%d") if isinstance(item.mulai,
                                                                   (datetime.date, datetime.datetime)) else str(
                item.mulai),
            "selesai": item.selesai.strftime("%Y-%m-%d") if isinstance(item.selesai,
                                                                       (datetime.date, datetime.datetime)) else str(
                item.selesai),
            "alasan": item.alasan,
            "status": item.status
        }

    @db_session
    def on_put(self, req, resp, id):
        """
        Digunakan untuk menangani aksi Approve, Reject, atau Update status Cuti dari Frontend.
        """
        try:
            body = req.media
            item = Cuti.get(id=int(id))

            if not item:
                resp.status = falcon.HTTP_404
                resp.media = {"status": False, "message": "Data cuti tidak ditemukan"}
                return

            # Menangani pembaruan status ("Approved" / "Rejected") dari handleApprove & handleReject di FE
            if "status" in body:
                item.status = body["status"]

            # Menangani perubahan field lainnya jika ada pengeditan manual masa mendatang
            if "nama" in body: item.nama = body["nama"]
            if "unit" in body: item.unit = body["unit"]
            if "alasan" in body: item.alasan = body["alasan"]

            if "mulai" in body and body["mulai"]:
                item.mulai = datetime.datetime.strptime(body["mulai"], "%Y-%m-%d")
            if "selesai" in body and body["selesai"]:
                item.selesai = datetime.datetime.strptime(body["selesai"], "%Y-%m-%d")

            pny.commit()

            resp.status = falcon.HTTP_200
            resp.media = {
                "status": True,
                "message": f"Data cuti berhasil diperbarui menjadi {item.status}"
            }

        except Exception as e:
            print("ERROR PUT CUTI:", e)
            resp.status = falcon.HTTP_500
            resp.media = {
                "status": False,
                "message": str(e)
            }

    @db_session
    def on_delete(self, req, resp, id):
        item = Cuti.get(id=int(id))

        if not item:
            resp.status = falcon.HTTP_404
            resp.media = {"status": False, "message": "Data cuti tidak ditemukan"}
            return

        item.delete()
        pny.commit()

        resp.status = falcon.HTTP_200
        resp.media = {
            "status": True,
            "message": "Data cuti berhasil dihapus"
        }
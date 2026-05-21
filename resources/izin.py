import datetime
import falcon
import pony.orm as pny
from pony.orm import db_session
from models.schema import Izin  # Menggunakan model Izin sesuai import utama


class IzinResource:

    @db_session
    def on_get(self, req, resp):
        # Mengambil semua data izin dari database
        query = Izin.select()

        # Disesuaikan 100% dengan FE: id, nama, unit, mulai, selesai, alasan, status
        data = [
            {
                "id": item.id,
                "nama": item.nama,
                "unit": item.unit if item.unit else "0",
                "mulai": (
                    item.mulai.strftime("%Y-%m-%d")
                    if isinstance(item.mulai, (datetime.date, datetime.datetime))
                    else str(item.mulai)
                ),
                "selesai": (
                    item.selesai.strftime("%Y-%m-%d")
                    if isinstance(item.selesai, (datetime.date, datetime.datetime))
                    else str(item.selesai)
                ),
                "alasan": item.alasan,
                "status": item.status if item.status else "Pending",
            }
            for item in query
        ]

        # Menghasilkan array langsung untuk di-fetch oleh FE
        resp.status = falcon.HTTP_200
        resp.media = data

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
                    "message": "Semua bidang data harus diisi!",
                }
                return

            # Parsing string ISO date dari FE ("YYYY-MM-DD") ke objek Python datetime sesuai permintaan
            try:
                mulai_dt = datetime.datetime.strptime(
                    body["mulai"], "%Y-%m-%d"
                )
                selesai_dt = datetime.datetime.strptime(
                    body["selesai"], "%Y-%m-%d"
                )
            except ValueError:
                resp.status = falcon.HTTP_400
                resp.media = {
                    "status": False,
                    "message": "Format tanggal mulai atau selesai tidak valid. Gunakan YYYY-MM-DD",
                }
                return

            # Menentukan unit otomatis secara dinamis persis seperti logic preConfirm Frontend
            nama_input = body["nama"]
            unit_default = "SD" if nama_input == "Andi Susanto" else "0"

            # Mapping field disesuaikan 100% dengan state data baru di Frontend
            baru = Izin(
                nama=nama_input,
                unit=body.get("unit", unit_default),
                mulai=mulai_dt,  # Menyimpan dalam tipe datetime
                selesai=selesai_dt,  # Menyimpan dalam tipe datetime
                alasan=body["alasan"],
                status="Pending",  # Pengajuan baru otomatis statusnya "Pending"
            )

            # Commit Pony ORM agar ID baru langsung tergenerasi
            pny.commit()

            resp.status = falcon.HTTP_201
            resp.media = {
                "id": baru.id,
                "nama": baru.nama,
                "unit": baru.unit,
                "mulai": baru.mulai.strftime("%Y-%m-%d"),
                "selesai": baru.selesai.strftime("%Y-%m-%d"),
                "alasan": baru.alasan,
                "status": baru.status,
            }

        except Exception as e:
            print("ERROR POST IZIN:", e)
            resp.status = falcon.HTTP_500
            resp.media = {"status": False, "message": str(e)}


class DetailIzinResource:

    @db_session
    def on_get(self, req, resp, id):
        item = Izin.get(id=int(id))

        if not item:
            resp.status = falcon.HTTP_404
            resp.media = {
                "status": False,
                "message": "Data izin tidak ditemukan",
            }
            return

        resp.status = falcon.HTTP_200
        resp.media = {
            "id": item.id,
            "nama": item.nama,
            "unit": item.unit,
            "mulai": (
                item.mulai.strftime("%Y-%m-%d")
                if isinstance(item.mulai, (datetime.date, datetime.datetime))
                else str(item.mulai)
            ),
            "selesai": (
                item.selesai.strftime("%Y-%m-%d")
                if isinstance(item.selesai, (datetime.date, datetime.datetime))
                else str(item.selesai)
            ),
            "alasan": item.alasan,
            "status": item.status,
        }

    @db_session
    def on_put(self, req, resp, id):
        """Digunakan untuk menangani aksi Approve (handleApprove) atau Reject (handleReject) status Izin dari Frontend."""
        try:
            body = req.media
            item = Izin.get(id=int(id))

            if not item:
                resp.status = falcon.HTTP_404
                resp.media = {
                    "status": False,
                    "message": "Data izin tidak ditemukan",
                }
                return

            # Menangani pembaruan status ("Approved" / "Rejected") dari handleApprove & handleReject di FE
            if "status" in body:
                item.status = body["status"]

            # Menangani perubahan field lainnya jika ada pengeditan di masa mendatang
            if "nama" in body:
                item.nama = body["nama"]
            if "unit" in body:
                item.unit = body["unit"]
            if "alasan" in body:
                item.alasan = body["alasan"]

            if "mulai" in body and body["mulai"]:
                item.mulai = datetime.datetime.strptime(
                    body["mulai"], "%Y-%m-%d"
                )
            if "selesai" in body and body["selesai"]:
                item.selesai = datetime.datetime.strptime(
                    body["selesai"], "%Y-%m-%d"
                )

            pny.commit()

            resp.status = falcon.HTTP_200
            resp.media = {
                "status": True,
                "message": f"Data izin berhasil diperbarui menjadi {item.status}",
            }

        except Exception as e:
            print("ERROR PUT IZIN:", e)
            resp.status = falcon.HTTP_500
            resp.media = {"status": False, "message": str(e)}

    @db_session
    def on_delete(self, req, resp, id):
        item = Izin.get(id=int(id))

        if not item:
            resp.status = falcon.HTTP_404
            resp.media = {
                "status": False,
                "message": "Data izin tidak ditemukan",
            }
            return

        item.delete()
        pny.commit()

        resp.status = falcon.HTTP_200
        resp.media = {
            "status": True,
            "message": "Data izin berhasil dihapus",
        }
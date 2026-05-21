import datetime
import falcon
import pony.orm as pny
from pony.orm import db_session
from models.schema import Lembur  # Menggunakan model Lembur asli sesuai FE


class LemburResource:

    @db_session
    def on_get(self, req, resp):
        # Mengambil semua data lembur dari database
        query = Lembur.select()

        # Disesuaikan 100% dengan FE: id, nama, unit, mulai, selesai, alasan, status
        data = [
            {
                "id": l.id,
                "nama": l.nama,
                "unit": l.unit if l.unit else "0",
                "mulai": (
                    l.mulai.strftime("%Y-%m-%d")
                    if isinstance(l.mulai, (datetime.date, datetime.datetime))
                    else str(l.mulai)
                ),
                "selesai": (
                    l.selesai.strftime("%Y-%m-%d")
                    if isinstance(l.selesai, (datetime.date, datetime.datetime))
                    else str(l.selesai)
                ),
                "alasan": l.alasan,
                "status": l.status if l.status else "Pending",
            }
            for l in query
        ]

        resp.media = data  # Menghasilkan array langsung sesuai kebutuhan fetch FE

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

            # Parsing string ISO date dari FE ("YYYY-MM-DD") ke objek Python datetime/date
            try:
                mulai_dt = datetime.datetime.strptime(body["mulai"], "%Y-%m-%d")
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

            # Mapping field disesuaikan 100% dengan state data baru di Frontend Lembur
            # Jika database Anda tidak auto-increment dan menerima ID manual dari Date.now() FE:
            # params = {"id": body["id"]} if "id" in body else {}

            baru = Lembur(
                nama=body["nama"],
                unit=body.get("unit", "0"),  # Default sesuai FE "0"
                mulai=mulai_dt,
                selesai=selesai_dt,
                alasan=body["alasan"],
                status="Pending",  # Pengajuan baru otomatis statusnya "Pending"
            )

            # Flush Pony ORM agar ID baru langsung tergenerasi (jika menggunakan auto-increment)
            pny.commit()

            resp.status = falcon.HTTP_201
            resp.media = {
                "id": baru.id,
                "nama": baru.nama,
                "unit": baru.unit,
                "mulai": body["mulai"],
                "selesai": body["selesai"],
                "alasan": baru.alasan,
                "status": baru.status,
            }

        except Exception as e:
            print("ERROR POST LEMBUR:", e)
            resp.status = falcon.HTTP_500
            resp.media = {"status": False, "message": str(e)}


class DetailLemburResource:

    @db_session
    def on_get(self, req, resp, id):
        item = Lembur.get(id=int(id))

        if not item:
            resp.status = falcon.HTTP_404
            resp.media = {
                "status": False,
                "message": "Data lembur tidak ditemukan",
            }
            return

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
        """Digunakan untuk menangani aksi Approve, Reject, atau Update status

        Lembur dari Frontend.
        """
        try:
            body = req.media
            item = Lembur.get(id=int(id))

            if not item:
                resp.status = falcon.HTTP_404
                resp.media = {
                    "status": False,
                    "message": "Data lembur tidak ditemukan",
                }
                return

            # Menangani pembaruan status ("Approved" / "Rejected") dari handleApprove & handleReject di FE
            if "status" in body:
                item.status = body["status"]

            # Menangani perubahan field lainnya jika ada pengeditan manual masa mendatang
            if "nama" in body:
                item.nama = body["nama"]
            if "unit" in body:
                item.unit = body["unit"]
            if "alasan" in body:
                item.alasan = body["alasan"]

            if "mulai" in body and body["mulai"]:
                item.mulai = datetime.datetime.strptime(body["mulai"], "%Y-%m-%d")
            if "selesai" in body and body["selesai"]:
                item.selesai = datetime.datetime.strptime(
                    body["selesai"], "%Y-%m-%d"
                )

            pny.commit()

            resp.status = falcon.HTTP_200
            resp.media = {
                "status": True,
                "message": f"Data lembur berhasil diperbarui menjadi {item.status}",
            }

        except Exception as e:
            print("ERROR PUT LEMBUR:", e)
            resp.status = falcon.HTTP_500
            resp.media = {"status": False, "message": str(e)}

    @db_session
    def on_delete(self, req, resp, id):
        item = Lembur.get(id=int(id))

        if not item:
            resp.status = falcon.HTTP_404
            resp.media = {
                "status": False,
                "message": "Data lembur tidak ditemukan",
            }
            return

        item.delete()
        pny.commit()

        resp.status = falcon.HTTP_200
        resp.media = {"status": True, "message": "Data lembur berhasil dihapus"}
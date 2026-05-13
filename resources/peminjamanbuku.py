import falcon
import traceback
from pony.orm import db_session, select
from models.schema import Peminjaman
from datetime import datetime


# =========================
# HELPERS
# =========================
def safe_int(value, default=0):
    try:
        return int(value)
    except:
        return default


def safe_str(value, default=""):
    return value if value is not None else default


def safe_datetime(value):
    try:
        if not value:
            return None
        return datetime.fromisoformat(value)
    except:
        return None


# =========================
# LIST + CREATE PEMINJAMAN
# =========================
class DataPeminjamanResource:

    @db_session
    def on_get(self, req, resp):

        query = select(p for p in Peminjaman)

        data = []

        for p in query:
            data.append({
                "id": p.id,
                "nama": p.nama,
                "buku": p.buku,
                "jumlah": p.jumlah,
                "pinjam": p.pinjam.isoformat() if p.pinjam else None,
                "kembali": p.kembali.isoformat() if p.kembali else None,
                "status": p.status
            })

        resp.media = {
            "status": True,
            "data": data
        }

    @db_session
    def on_post(self, req, resp):

        body = req.media or {}

        try:
            peminjaman = Peminjaman(
                nama=safe_str(body.get("nama")),
                buku=safe_str(body.get("buku")),
                jumlah=safe_int(body.get("jumlah"), 1),
                pinjam=safe_datetime(body.get("pinjam")) or datetime.now(),
                kembali=safe_datetime(body.get("kembali")),
                status=safe_str(body.get("status"), "Dipinjam")
            )

            resp.media = {
                "status": True,
                "message": "Peminjaman berhasil ditambahkan",
                "id": peminjaman.id
            }

        except Exception as e:
            print("ERROR:", e)
            print(traceback.format_exc())

            resp.status = falcon.HTTP_400
            resp.media = {
                "status": False,
                "message": str(e)
            }


# =========================
# DETAIL + UPDATE + DELETE
# =========================
class DetailPeminjamanResource:

    @db_session
    def on_get(self, req, resp, id):

        p = Peminjaman.get(id=id)

        if not p:
            raise falcon.HTTPNotFound()

        resp.media = {
            "status": True,
            "data": {
                "id": p.id,
                "nama": p.nama,
                "buku": p.buku,
                "jumlah": p.jumlah,
                "pinjam": p.pinjam.isoformat() if p.pinjam else None,
                "kembali": p.kembali.isoformat() if p.kembali else None,
                "status": p.status
            }
        }

    @db_session
    def on_put(self, req, resp, id):

        try:
            body = req.media or {}

            p = Peminjaman.get(id=id)

            if not p:
                raise falcon.HTTPNotFound()

            p.set(
                nama=safe_str(body.get("nama")),
                buku=safe_str(body.get("buku")),
                jumlah=safe_int(body.get("jumlah"), 1),
                pinjam=safe_datetime(body.get("pinjam")),
                kembali=safe_datetime(body.get("kembali")),
                status=safe_str(body.get("status"), "Dipinjam")
            )

            resp.media = {
                "status": True,
                "message": "Peminjaman berhasil diupdate"
            }

        except Exception as e:
            print("ERROR:", e)
            print(traceback.format_exc())

            resp.status = falcon.HTTP_400
            resp.media = {
                "status": False,
                "message": str(e)
            }

    @db_session
    def on_delete(self, req, resp, id):

        p = Peminjaman.get(id=id)

        if not p:
            raise falcon.HTTPNotFound()

        p.delete()

        resp.media = {
            "status": True,
            "message": "Peminjaman berhasil dihapus"
        }
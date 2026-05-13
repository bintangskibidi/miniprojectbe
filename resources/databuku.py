import falcon
import traceback
from pony.orm import db_session, select, commit
from models.schema import Buku, Peminjaman
from datetime import datetime


# =========================
# HELPERS
# =========================
def safe_int(value, default=0):
    try:
        if value is None: return default
        return int(value)
    except:
        return default


def safe_str(value, default=""):
    if value is None:
        return default
    return str(value)


def safe_datetime(value):
    try:
        if not value:
            return None
        return datetime.fromisoformat(value)
    except:
        return None


# =========================
# LIST + CREATE BUKU
# =========================
class DataBukuResource:

    @db_session
    def on_get(self, req, resp):
        search = req.get_param("search")

        # Inisialisasi query awal
        query = select(b for b in Buku)

        if search:
            # Kita buat keyword lowercase di Python dulu
            kw = search.lower()
            # Gunakan sintaks 'or' di dalam filter untuk menangani NULL/None
            # Pony ORM akan menerjemahkan ini ke SQL LOWER() secara otomatis
            query = select(b for b in Buku if
                           kw in b.judul.lower() or
                           kw in b.penulis.lower() or
                           kw in b.barcode.lower())

        data = []
        for b in query:
            data.append({
                "id": b.id,
                "barcode": b.barcode,
                "judul": b.judul,
                "penulis": b.penulis,
                "penerbit": b.penerbit,
                "tahun": b.tahun,
                "isbn": b.isbn,
                "harga": b.harga,
                "kondisi": b.kondisi,
                "kategori": b.kategori,
                "rak": b.rak,
                "stok": b.stok
            })

        resp.media = {"status": True, "data": data}

    @db_session
    def on_post(self, req, resp):
        body = req.media or {}
        try:
            buku = Buku(
                barcode=safe_str(body.get("barcode")) or f"BK{int(datetime.now().timestamp())}",
                judul=safe_str(body.get("judul")),
                penulis=safe_str(body.get("penulis")),
                penerbit=safe_str(body.get("penerbit")),
                tahun=safe_int(body.get("tahun"), None),
                isbn=safe_str(body.get("isbn")),
                harga=safe_int(body.get("harga"), 0),
                kondisi=safe_str(body.get("kondisi"), "Baik"),
                kategori=safe_str(body.get("kategori")),
                rak=safe_str(body.get("rak")),
                stok=safe_int(body.get("stok"), 1)
            )
            commit()
            resp.media = {
                "status": True,
                "message": "Buku berhasil ditambahkan",
                "id": buku.id
            }
        except Exception as e:
            resp.status = falcon.HTTP_400
            resp.media = {"status": False, "message": str(e)}


# =========================
# DETAIL + UPDATE + DELETE BUKU
# =========================
class DetailBukuResource:

    @db_session
    def on_get(self, req, resp, id):
        buku = Buku.get(id=id)
        if not buku: raise falcon.HTTPNotFound()

        resp.media = {
            "status": True,
            "data": {
                "id": buku.id, "barcode": buku.barcode, "judul": buku.judul,
                "penulis": buku.penulis, "penerbit": buku.penerbit, "tahun": buku.tahun,
                "isbn": buku.isbn, "harga": buku.harga, "kondisi": buku.kondisi,
                "kategori": buku.kategori, "rak": buku.rak, "stok": buku.stok
            }
        }

    @db_session
    def on_put(self, req, resp, id):
        try:
            data = req.media or {}
            buku = Buku.get(id=id)
            if not buku:
                raise falcon.HTTPNotFound()

            buku.set(
                barcode=safe_str(data.get("barcode")),
                judul=safe_str(data.get("judul")),
                penulis=safe_str(data.get("penulis")),
                penerbit=safe_str(data.get("penerbit")),
                tahun=safe_int(data.get("tahun"), None),
                isbn=safe_str(data.get("isbn")),
                harga=safe_int(data.get("harga"), 0),
                kondisi=safe_str(data.get("kondisi"), "Baik"),
                kategori=safe_str(data.get("kategori")),
                rak=safe_str(data.get("rak")),
                stok=safe_int(data.get("stok"), 1)
            )

            resp.media = {"status": True, "message": "Data buku berhasil diupdate"}
        except Exception as e:
            resp.status = falcon.HTTP_400
            resp.media = {"status": False, "message": str(e)}

    @db_session
    def on_delete(self, req, resp, id):
        buku = Buku.get(id=id)
        if not buku:
            raise falcon.HTTPNotFound()
        buku.delete()
        resp.media = {"status": True, "message": "Data buku berhasil dihapus"}
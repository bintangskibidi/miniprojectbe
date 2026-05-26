import falcon
import pony.orm as pny
from pony.orm import db_session
# Pastikan import model di bawah ini mengarah ke definisi entitas KomponenGaji Anda
from models.schema import KomponenGaji


class KomponenGajiResource:

    @db_session
    def on_get(self, req, resp):
        """
        Mengambil semua daftar komponen gaji.
        Disesuaikan 100% dengan struktur array state data di FE.
        """
        try:
            # Mengambil semua data komponen gaji dari database
            query = KomponenGaji.select().order_by(lambda k: k.id)

            data = [
                {
                    "id": k.id,
                    "nama": k.nama,
                    "jenis": k.jenis,
                    "perhitungan": k.perhitungan,
                    "nominal": k.nominal,
                    "keterangan": k.keterangan if k.keterangan else ""
                }
                for k in query
            ]

            resp.status = falcon.HTTP_200
            resp.media = data  # Menghasilkan array langsung untuk kebutuhan setData() di FE

        except Exception as e:
            print("ERROR GET KOMPONEN GAJI:", e)
            resp.status = falcon.HTTP_500
            resp.media = {"status": False, "message": str(e)}

    @db_session
    def on_post(self, req, resp):
        """
        Menambah komponen gaji baru.
        Validasi meniru persis preConfirm SweetAlert di Frontend.
        """
        try:
            body = req.media or {}

            nama = body.get("nama")
            jenis = body.get("jenis")
            perhitungan = body.get("perhitungan")
            nominal = body.get("nominal")
            keterangan = body.get("keterangan", "")

            # Validasi meniru persis: if (!nama || !jenis || !perhitungan || !nominal)
            if not nama or not jenis or not perhitungan or not nominal:
                resp.status = falcon.HTTP_400
                resp.media = {
                    "status": False,
                    "message": "Semua field wajib diisi"
                }
                return

            # Simpan data baru ke database
            # Jika FE mengirimkan id berbasis Date.now(), kita tangkap atau fallback ke Auto-increment DB
            baru = KomponenGaji(
                id=body.get("id") if "id" in body else None,
                nama=str(nama).strip(),
                jenis=str(jenis).strip(),
                perhitungan=str(perhitungan).strip(),
                nominal=str(nominal).strip(),
                keterangan=str(keterangan).strip()
            )

            pny.commit()

            resp.status = falcon.HTTP_201
            resp.media = {
                "id": baru.id,
                "nama": baru.nama,
                "jenis": baru.jenis,
                "perhitungan": baru.perhitungan,
                "nominal": baru.nominal,
                "keterangan": baru.keterangan
            }

        except Exception as e:
            print("ERROR POST KOMPONEN GAJI:", e)
            resp.status = falcon.HTTP_500
            resp.media = {"status": False, "message": str(e)}


class DetailKomponenGajiResource:

    @db_session
    def on_get(self, req, resp, id):
        """
        Melihat detail komponen gaji spesifik berdasarkan ID
        """
        try:
            item = KomponenGaji.get(id=int(id))

            if not item:
                resp.status = falcon.HTTP_404
                resp.media = {
                    "status": False,
                    "message": "Data komponen gaji tidak ditemukan",
                }
                return

            resp.status = falcon.HTTP_200
            resp.media = {
                "id": item.id,
                "nama": item.nama,
                "jenis": item.jenis,
                "perhitungan": item.perhitungan,
                "nominal": item.nominal,
                "keterangan": item.keterangan if item.keterangan else "",
            }
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": False, "message": str(e)}

    @db_session
    def on_put(self, req, resp, id):
        """
        Mengupdate data komponen gaji berdasarkan ID.
        Menangani sinkronisasi fungsi editData(item) dari FE saat submit Update.
        """
        try:
            item = KomponenGaji.get(id=int(id))

            if not item:
                resp.status = falcon.HTTP_404
                resp.media = {
                    "status": False,
                    "message": "Data komponen gaji tidak ditemukan",
                }
                return

            body = req.media or {}
            nama = body.get("nama")
            jenis = body.get("jenis")
            perhitungan = body.get("perhitungan")
            nominal = body.get("nominal")
            keterangan = body.get("keterangan", "")

            # Validasi edit: semua field wajib diisi
            if not nama or not jenis or not perhitungan or not nominal:
                resp.status = falcon.HTTP_400
                resp.media = {
                    "status": False,
                    "message": "Semua field wajib diisi"
                }
                return

            # Update data ke database
            item.nama = str(nama).strip()
            item.jenis = str(jenis).strip()
            item.perhitungan = str(perhitungan).strip()
            item.nominal = str(nominal).strip()
            item.keterangan = str(keterangan).strip()

            pny.commit()

            resp.status = falcon.HTTP_200
            resp.media = {
                "id": item.id,
                "nama": item.nama,
                "jenis": item.jenis,
                "perhitungan": item.perhitungan,
                "nominal": item.nominal,
                "keterangan": item.keterangan
            }

        except Exception as e:
            print("ERROR UPDATE KOMPONEN GAJI:", e)
            resp.status = falcon.HTTP_500
            resp.media = {"status": False, "message": str(e)}

    @db_session
    def on_delete(self, req, resp, id):
        """
        Menghapus data komponen gaji berdasarkan ID.
        Digunakan untuk menangani fungsi hapusData(id) dari FE.
        """
        try:
            item = KomponenGaji.get(id=int(id))

            if not item:
                resp.status = falcon.HTTP_404
                resp.media = {
                    "status": False,
                    "message": "Data komponen gaji tidak ditemukan",
                }
                return

            item.delete()
            pny.commit()

            resp.status = falcon.HTTP_200
            resp.media = {
                "status": True,
                "message": "Data berhasil dihapus"
            }

        except Exception as e:
            print("ERROR DELETE KOMPONEN GAJI:", e)
            resp.status = falcon.HTTP_500
            resp.media = {"status": False, "message": str(e)}
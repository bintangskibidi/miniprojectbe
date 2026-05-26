import falcon
import json
from datetime import datetime
import pony.orm as pny
from pony.orm import db_session

# Pastikan import model di bawah ini sesuai dengan file skema database Anda
# dari models.schema import RekapPresensi
from models.schema import RekapPresensi


class AbsensiHarianResource:

    @db_session
    def on_get(self, req, resp):
        """
        Mengambil semua data absensi harian.
        Format output disesuaikan 100% dengan array state 'dataAbsensi' di FE.
        """
        try:
            # Ambil semua data absensi, urutkan berdasarkan tanggal terbaru
            query = RekapPresensi.select().order_by(pny.desc(RekapPresensi.tanggal))

            data = [
                {
                    "id": item.id,
                    "tanggal": str(item.tanggal),  # Format YYYY-MM-DD
                    "nip": item.nip,
                    "nama": item.nama,
                    "jenisPegawai": item.jenis_pegawai,
                    "unit": item.unit if item.unit else "0",
                    "jamMasuk": item.jam_masuk if item.jam_masuk else "",
                    "statusMasuk": item.status_masuk if item.status_masuk else "Tepat Waktu",
                    "jamPulang": item.jam_pulang if item.jam_pulang else "",
                    "statusPulang": item.status_pulang if item.status_pulang else "Sesuai Jadwal",
                    "keterangan": item.keterangan if item.keterangan else "Hadir",
                    "terlambat": item.terlambat if item.terlambat else "0 mnt",
                    "pulangAwal": item.pulang_awal if item.pulang_awal else "0 mnt"
                }
                for item in query
            ]

            resp.status = falcon.HTTP_200
            resp.media = data

        except Exception as e:
            print("ERROR GET ABSENSI HARIAN:", e)
            resp.status = falcon.HTTP_500
            resp.media = {"status": False, "message": str(e)}

    @db_session
    def on_post(self, req, resp):
        """
        Menambah data absensi harian baru.
        Logika kalkulasi status & durasi meniru 100% preConfirm Frontend.
        """
        try:
            body = req.media or {}

            tanggal = body.get("tanggal")
            nip = body.get("nip")
            nama = body.get("nama")
            jenis_pegawai = body.get("jenisPegawai")
            unit = body.get("unit", "0")
            jam_masuk = body.get("jamMasuk")
            jam_pulang = body.get("jamPulang")
            keterangan = body.get("keterangan", "Hadir")

            # 1. Validasi Persis FE (Semua form wajib diisi jika Hadir)
            if not tanggal or not jam_masuk or not jam_pulang:
                resp.status = falcon.HTTP_400
                resp.media = {"status": False, "message": "Semua form harus diisi!"}
                return

            # 2. Kalkulasi Status & Keterlambatan Sederhana (Meniru Logika FE)
            # Batas Masuk 07:30, Batas Pulang 16:00
            status_masuk = "Terlambat" if jam_masuk > "07:30" else "Tepat Waktu"
            status_pulang = "Pulang Awal" if jam_pulang < "16:00" else "Sesuai Jadwal"
            terlambat = "30 mnt" if jam_masuk > "07:30" else "0 mnt"
            pulang_awal = "15 mnt" if jam_pulang < "16:00" else "0 mnt"

            # Jika statusnya selain Hadir (Izin/Sakit/Alpa), sesuaikan nilainya jika diperlukan
            if keterangan != "Hadir":
                status_masuk = "-"
                status_pulang = "-"
                terlambat = "0 mnt"
                pulang_awal = "0 mnt"

            # 3. Simpan ke Database
            baru = RekapPresensi(
                tanggal=tanggal,
                nip=nip,
                nama=nama,
                jenis_pegawai=jenis_pegawai,
                unit=unit,
                jam_masuk=jam_masuk,
                status_masuk=status_masuk,
                jam_pulang=jam_pulang,
                status_pulang=status_pulang,
                keterangan=keterangan,
                terlambat=terlambat,
                pulang_awal=pulang_awal
            )

            pny.commit()

            resp.status = falcon.HTTP_201
            resp.media = {
                "id": baru.id,
                "tanggal": str(baru.tanggal),
                "nip": baru.nip,
                "nama": baru.nama,
                "jenisPegawai": baru.jenis_pegawai,
                "unit": baru.unit,
                "jamMasuk": baru.jam_masuk,
                "statusMasuk": baru.status_masuk,
                "jamPulang": baru.jam_pulang,
                "statusPulang": baru.status_pulang,
                "keterangan": baru.keterangan,
                "terlambat": baru.terlambat,
                "pulangAwal": baru.pulang_awal
            }

        except Exception as e:
            print("ERROR POST ABSENSI HARIAN:", e)
            resp.status = falcon.HTTP_500
            resp.media = {"status": False, "message": str(e)}


class DetailAbsensiHarianResource:

    @db_session
    def on_put(self, req, resp, id):
        """
        Mengubah data absensi harian berdasarkan ID (Fungsi Edit).
        Logika kalkulasi meniru 100% preConfirm Edit Frontend.
        """
        try:
            item = RekapPresensi.get(id=int(id))
            if not item:
                resp.status = falcon.HTTP_404
                resp.media = {"status": False, "message": "Data absensi tidak ditemukan"}
                return

            body = req.media or {}
            tanggal = body.get("tanggal")
            jam_masuk = body.get("jamMasuk")
            jam_pulang = body.get("jamPulang")
            keterangan = body.get("keterangan")

            # Validasi form edit
            if not tanggal or not jam_masuk or not jam_pulang:
                resp.status = falcon.HTTP_400
                resp.media = {"status": False, "message": "Semua form wajib diisi!"}
                return

            # Kalkulasi Ulang Logika Status (Persis FE)
            status_masuk = "Terlambat" if jam_masuk > "07:30" else "Tepat Waktu"
            status_pulang = "Pulang Awal" if jam_pulang < "16:00" else "Sesuai Jadwal"
            terlambat = "30 mnt" if jam_masuk > "07:30" else "0 mnt"
            pulang_awal = "15 mnt" if jam_pulang < "16:00" else "0 mnt"

            if keterangan != "Hadir":
                status_masuk = "-"
                status_pulang = "-"
                terlambat = "0 mnt"
                pulang_awal = "0 mnt"

            # Update data ke database
            item.tanggal = tanggal
            item.jam_masuk = jam_masuk
            item.jam_pulang = jam_pulang
            item.keterangan = keterangan
            item.status_masuk = status_masuk
            item.status_pulang = status_pulang
            item.terlambat = terlambat
            item.pulang_awal = pulang_awal

            pny.commit()

            resp.status = falcon.HTTP_200
            resp.media = {"status": True, "message": "Data absensi diperbarui."}

        except Exception as e:
            print("ERROR PUT ABSENSI HARIAN:", e)
            resp.status = falcon.HTTP_500
            resp.media = {"status": False, "message": str(e)}

    @db_session
    def on_delete(self, req, resp, id):
        """
        Menghapus data absensi berdasarkan ID.
        """
        try:
            item = RekapPresensi.get(id=int(id))
            if not item:
                resp.status = falcon.HTTP_404
                resp.media = {"status": False, "message": "Data absensi tidak ditemukan"}
                return

            item.delete()
            pny.commit()

            resp.status = falcon.HTTP_200
            resp.media = {"status": True, "message": "Data absensi telah dihapus."}

        except Exception as e:
            print("ERROR DELETE ABSENSI HARIAN:", e)
            resp.status = falcon.HTTP_500
            resp.media = {"status": False, "message": str(e)}


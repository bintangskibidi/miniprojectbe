import datetime
import random
import falcon
from pony.orm import db_session, select, desc, flush
from models.schema import BackupFile


class BackupDataResource:

    # Helper untuk memformat output JSON agar pas dengan format UI React
    def _format_output(self, backup_obj):
        bulan_indo = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agt", "Sep", "Okt", "Nov", "Des"]
        dt = backup_obj.waktu_backup  # Ini mengambil waktu nyata dari database

        return {
            "id": backup_obj.id,
            "nama": backup_obj.nama,
            "ukuran": backup_obj.ukuran,
            # Format Tanggal: "19 Mei 2026"
            "tanggal": f"{dt.day:02d} {bulan_indo[dt.month - 1]} {dt.year}",
            # Format Waktu (24 Jam) sesuai waktu IRL sekarang: "11:07:00"
            "waktu": dt.strftime("%H:%M:%S")
        }

    # ==========================================
    # 1. GET: Ambil Semua List Backup
    # ==========================================
    @db_session
    def on_get(self, req, resp):
        # Ambil data backup, urutkan dari yang paling baru dibuat
        query = select(b for b in BackupFile).order_by(desc(BackupFile.waktu_backup))

        # Format setiap data menggunakan helper di atas
        data_backup = [self._format_output(b) for b in query]
        resp.media = data_backup

    # ==========================================
    # 2. POST: Membuat Data Backup Baru
    # ==========================================
    @db_session
    def on_post(self, req, resp):
        # Mengambil waktu nyata saat ini (In Real Life / IRL) dari sistem server
        waktu_sekarang = datetime.datetime.now()

        # Format nama file dengan tanggal & jam pembuatan
        timestamp_nama = waktu_sekarang.strftime("%Y%m%d_%H%M%S")
        nama_file = f"backup_partial_{timestamp_nama}.sql"

        # Ukuran file simulasi
        ukuran_simulasi = f"{random.uniform(1.5, 3.5):.1f} MB"

        # Simpan objek datetime langsung ke MySQL
        baru = BackupFile(
            nama=nama_file,
            ukuran=ukuran_simulasi,
            waktu_backup=waktu_sekarang
        )

        # Force push ke database agar ID auto_increment langsung dibuat oleh MySQL
        flush()

        resp.status = falcon.HTTP_201
        resp.media = {
            "status": True,
            "message": "File backup berhasil dibuat",
            "data": self._format_output(baru)  # Dikirim dengan format tanggal & waktu terpisah untuk React
        }

    # ==========================================
    # 3. DELETE: Hapus Backup Berdasarkan ID
    # ==========================================
    @db_session
    def on_delete(self, req, resp, id=None):
        if not id:
            resp.status = falcon.HTTP_400
            resp.media = {"status": False, "message": "ID backup tidak disertakan"}
            return

        file_backup = BackupFile.get(id=id)

        if not file_backup:
            resp.status = falcon.HTTP_404
            resp.media = {"status": False, "message": "File backup tidak ditemukan"}
            return

        file_backup.delete()

        resp.media = {
            "status": True,
            "message": "File backup berhasil dihapus"
        }
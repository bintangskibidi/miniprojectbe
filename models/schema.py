from pony.orm import PrimaryKey, Required, Optional, LongStr
from datetime import date
from database import db

class EkstraKulikuler(db.Entity):
    _table_ = "ekstrakurikuler"
    id = PrimaryKey(int, auto=True)
    nama_kelas = Required(str)    # Ini untuk 'nama' ekskul
    nama_pegawai = Required(str)  # Ini untuk 'pembina'
    jadwal = Optional(str)        # Tambahan baru
    tanggal = Optional(str)
    keterangan = Optional(str)

class JenisSemester(db.Entity):
    _table_ = "jenis_semester"
    id = PrimaryKey(int, auto=True)
    nama = Required(str, 100)
    status = Required(bool, default=True)

    def to_dict(self):
        return {
            "id": self.id,
            "nama": self.nama,
            "status": self.status
        }

class AspekPenilaian(db.Entity):
    _table_ = "aspek_penilaian"
    id = PrimaryKey(int, auto=True)
    kode_aspek = Required(str, unique=True, max_len=20)
    nama_aspek = Required(str, max_len=100)

class TahunAjaran(db.Entity):
    id = PrimaryKey(int, auto=True)
    tahun_ajaran = Required(str, unique=True)
    tahun = Required(str)
    status = Required(bool, default=True)

class User(db.Entity):
    id = PrimaryKey(int, auto=True)
    email = Required(str, unique=True)
    password = Required(str)

class Kelas(db.Entity):
    id = PrimaryKey(int, auto=True)
    kode_kelas = Required(str, unique=True)
    nama_kelas = Required(str)

class Jurusan(db.Entity):
    id = PrimaryKey(int, auto=True)
    kode_jurusan = Required(str, unique=True)
    nama_jurusan = Required(str)

class WaliKelas(db.Entity):
    id = PrimaryKey(int, auto=True)
    nama_pegawai = Required(str)
    nama_kelas = Required(str)
    tahun_ajaran = Optional(str)

class Siswa(db.Entity):
    id = PrimaryKey(int, auto=True)
    nis = Required(str, unique=True)
    nisn = Optional(str)
    nama = Required(str)
    # ... atribut lainnya tetap sama ...
    tempat_lahir = Optional(str)
    tanggal_lahir = Optional(date)
    jenis_kelamin = Optional(str)
    alamat = Optional(LongStr)
    agama = Optional(str)
    golongan_darah = Optional(str)
    status = Optional(str)
    tahun_ajaran = Optional(str)
    tahun_masuk = Optional(str)
    kelas = Optional(str)
    jurusan = Optional(str)
    hp = Optional(str)
    sekolah_asal = Optional(str)
    ayah = Optional(str)
    ibu = Optional(str)
    wali = Optional(str)
    pekerjaan_ayah = Optional(str)
    pekerjaan_ibu = Optional(str)
    hp_ayah = Optional(str)
    hp_ibu = Optional(str)
    hp_wali = Optional(str)
    hubungan_wali = Optional(str)
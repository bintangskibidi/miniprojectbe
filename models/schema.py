# models/schema.py

from pony.orm import Required, Optional, PrimaryKey, LongStr
from datetime import date
from app import db


# =========================
# USER LOGIN
# =========================
class User(db.Entity):
    _table_ = "users"

    id = PrimaryKey(int, auto=True)
    email = Required(str, unique=True, max_len=100)
    password = Required(str, max_len=255)


# =========================
# DATA SISWA
# =========================
class Siswa(db.Entity):
    _table_ = "siswa"

    id = PrimaryKey(int, auto=True)

    # identitas utama
    nis = Required(str, unique=True, max_len=30)
    nisn = Optional(str, max_len=30)
    nama = Required(str, max_len=150)

    # biodata
    tempat_lahir = Optional(str, max_len=100)
    tanggal_lahir = Optional(date)
    jenis_kelamin = Optional(str, max_len=20)

    # alamat
    alamat = Optional(LongStr)

    # sekolah
    agama = Optional(str, max_len=30)
    status = Optional(str, max_len=30)      # Aktif / Alumni
    kelas = Optional(str, max_len=30)
    jurusan = Optional(str, max_len=50)
    hp = Optional(str, max_len=30)
    sekolah_asal = Optional(str, max_len=150)

    # orang tua
    ayah = Optional(str, max_len=150)
    ibu = Optional(str, max_len=150)
    wali = Optional(str, max_len=150)
from datetime import date
from pony.orm import LongStr, Optional, PrimaryKey, Required, Set
from database import db


class EkstraKulikuler(db.Entity):
    _table_ = "ekstrakurikuler"
    id = PrimaryKey(int, auto=True)
    nama_kelas = Required(str)
    nama_pegawai = Required(str)
    jadwal = Optional(str)
    tanggal = Optional(str)
    keterangan = Optional(str)


class JenisSemester(db.Entity):
    _table_ = "jenis_semester"
    id = PrimaryKey(int, auto=True)
    nama = Required(str, 100)
    status = Required(bool, default=True)

    semesters = Set("Semester")


class AspekPenilaian(db.Entity):
    _table_ = "aspek_penilaian"
    id = PrimaryKey(int, auto=True)
    kode_aspek = Required(str, unique=True, max_len=20)
    nama_aspek = Required(str, max_len=100)

    # 🔥 TAMBAH INI
    raports = Set("Raport")


class TahunAjaran(db.Entity):
    _table_ = "tahun_ajaran"
    id = PrimaryKey(int, auto=True)
    tahun_ajaran = Required(str, unique=True)
    tahun = Required(str)
    status = Required(bool, default=True)

    semesters = Set("Semester")

    # optional (aman kalau ada)
    raports = Set("Raport")


class Semester(db.Entity):
    _table_ = "semester"
    id = PrimaryKey(int, auto=True)
    tahun_ajaran = Required(TahunAjaran)
    jenis_semester = Required(JenisSemester)
    nama_semester = Required(str, 100)
    status = Required(bool, default=True)

    # 🔥 TAMBAH INI
    raports = Set("Raport")


class User(db.Entity):
    id = PrimaryKey(int, auto=True)
    email = Required(str, unique=True)
    password = Required(str)

    # optional
    raports = Set("Raport")


class Kelas(db.Entity):
    id = PrimaryKey(int, auto=True)
    kode_kelas = Required(str, unique=True)
    nama_kelas = Required(str)

    # 🔥 TAMBAH INI
    raports = Set("Raport")


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

    # 🔥 WAJIB
    raports = Set("Raport")


class Raport(db.Entity):
    _table_ = "raport"

    id = PrimaryKey(int, auto=True)

    siswa = Required(Siswa)
    kelas = Required(Kelas)
    semester = Required(Semester)
    mapel = Required(AspekPenilaian)

    tahun_ajaran = Optional(TahunAjaran)
    wali = Optional(User)

    kkm = Optional(int)
    harian = Optional(int)
    ujian = Optional(int)
    deskripsi = Optional(str)
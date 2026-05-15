from datetime import date, datetime
from pony.orm import LongStr, Optional, PrimaryKey, Required, Set
from database import db


# ==========================================
# AUTH & USER
# ==========================================
class User(db.Entity):
    id = PrimaryKey(int, auto=True)
    email = Required(str, unique=True)
    password = Required(str)
    raports = Set("Raport")


# ==========================================
# AKADEMIK DATA
# ==========================================
class Mapel(db.Entity):
    _table_ = "mapel"
    id = PrimaryKey(int, auto=True)
    nama = Required(str, unique=True)
    jadwal_mengajar = Set("JadwalMengajar")

    def to_dict(self):
        return {"id": self.id, "nama": self.nama}


class Jurusan(db.Entity):
    _table_ = "jurusan"
    id = PrimaryKey(int, auto=True)
    kode_jurusan = Required(str, unique=True)
    nama_jurusan = Required(str)


class Kelas(db.Entity):
    id = PrimaryKey(int, auto=True)
    kode_kelas = Required(str, unique=True)
    nama_kelas = Required(str)
    raports = Set("Raport")
    presensis = Set("Presensi")
    jadwal_mengajar = Set("JadwalMengajar")


class TahunAjaran(db.Entity):
    _table_ = "tahun_ajaran"
    id = PrimaryKey(int, auto=True)
    tahun_ajaran = Required(str, unique=True)
    tahun = Required(str)
    status = Required(bool, default=True)
    semesters = Set("Semester")
    raports = Set("Raport")
    presensis = Set("Presensi")

    def to_dict(self):
        return {
            "id": self.id,
            "tahun_ajaran": self.tahun_ajaran,
            "tahun": self.tahun,
            "status": self.status
        }


class JenisSemester(db.Entity):
    _table_ = "jenis_semester"
    id = PrimaryKey(int, auto=True)
    nama = Required(str, 100)
    status = Required(bool, default=True)
    semesters = Set("Semester")

    def to_dict(self):
        return {"id": self.id, "nama": self.nama, "status": self.status}


class Semester(db.Entity):
    _table_ = "semester"
    id = PrimaryKey(int, auto=True)
    tahun_ajaran = Required(TahunAjaran)
    jenis_semester = Required(JenisSemester)
    nama_semester = Required(str, 100)
    status = Required(bool, default=True)
    raports = Set("Raport")
    presensis = Set("Presensi")


class AspekPenilaian(db.Entity):
    _table_ = "aspek_penilaian"
    id = PrimaryKey(int, auto=True)
    kode_aspek = Required(str, unique=True, max_len=20)
    nama_aspek = Required(str, max_len=100)
    raports = Set("Raport")

    def to_dict(self):
        return {"id": self.id, "kode_aspek": self.kode_aspek, "nama_aspek": self.nama_aspek}


# ==========================================
# SISWA
# ==========================================
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

    raports = Set("Raport")
    presensis = Set("Presensi")


# ==========================================
# BUKU
# ==========================================
class Buku(db.Entity):
    _table_ = "buku"

    id = PrimaryKey(int, auto=True)
    barcode = Optional(str)
    judul = Required(str)
    penulis = Optional(str)
    penerbit = Optional(str)
    tahun = Optional(date)
    isbn = Optional(str)
    harga = Optional(int, default=0)
    kondisi = Optional(str)
    kategori = Optional(str)
    rak = Optional(str)
    stok = Optional(int, default=1)



    def to_dict(self):
        return {
            "id": self.id,
            "barcode": self.barcode,
            "judul": self.judul,
            "penulis": self.penulis,
            "penerbit": self.penerbit,
            "tahun": self.tahun.isoformat() if self.tahun else None,
            "isbn": self.isbn,
            "harga": self.harga,
            "kondisi": self.kondisi,
            "kategori": self.kategori,
            "rak": self.rak,
            "stok": self.stok
        }


# ==========================================
# PEMINJAMAN BUKU (STRING VERSION)
# ==========================================
class Peminjaman(db.Entity):
    _table_ = "peminjaman"

    id = PrimaryKey(int, auto=True)

    # sesuai request kamu: pakai string
    nama = Required(str)
    buku = Required(str)

    jumlah = Required(int, default=1)

    pinjam = Required(datetime, default=datetime.now)
    kembali = Optional(datetime)

    status = Required(str, default="Dipinjam")


# ==========================================
# PEGAWAI
# ==========================================
class Pegawai(db.Entity):
    _table_ = "pegawai"

    id = PrimaryKey(int, auto=True)

    nama = Required(str)
    nip = Optional(str)

    pendidikan = Optional(str)
    golongan = Optional(str)
    status_pegawai = Optional(str)

    tanggal_sk = Optional(str)
    masa_kerja = Optional(str)

    jabatan = Required(str)

    no_hp = Optional(str)
    email = Optional(str)

    jenis_pegawai = Optional(str)

    unit = Optional(str)

    status = Optional(str)

    jadwal_mengajar = Set("JadwalMengajar")

    def to_dict(self):
        return {
            "id": self.id,
            "nama": self.nama,
            "nip": self.nip,
            "pendidikan": self.pendidikan,
            "golongan": self.golongan,
            "status_pegawai": self.status_pegawai,
            "tanggal_sk": self.tanggal_sk,
            "masa_kerja": self.masa_kerja,
            "jabatan": self.jabatan,
            "no_hp": self.no_hp,
            "email": self.email,
            "jenis_pegawai": self.jenis_pegawai,
            "unit": self.unit,
            "status": self.status
        }


class WaliKelas(db.Entity):
    id = PrimaryKey(int, auto=True)
    nama_pegawai = Required(str)
    nama_kelas = Required(str)
    tahun_ajaran = Optional(str)


class EkstraKulikuler(db.Entity):
    _table_ = "ekstrakurikuler"
    id = PrimaryKey(int, auto=True)
    nama_kelas = Required(str)
    nama_pegawai = Required(str)
    jadwal = Optional(str)
    tanggal = Optional(str)
    keterangan = Optional(str)


# ==========================================
# TRANSAKSIONAL
# ==========================================
class Presensi(db.Entity):
    _table_ = "presensi"
    id = PrimaryKey(int, auto=True)
    siswa = Required(Siswa)
    kelas = Required(Kelas)
    tanggal = Required(str)
    jam_masuk = Optional(str)
    jam_pulang = Optional(str)
    status_masuk = Optional(str)
    keterangan = Required(str)
    detail_ijin = Optional(str)
    tahun_ajaran = Optional(TahunAjaran)
    semester = Optional(Semester)


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


class JadwalMengajar(db.Entity):
    _table_ = "jadwal_mengajar"
    id = PrimaryKey(int, auto=True)
    pegawai = Required(Pegawai)
    mapel = Required(Mapel)
    kelas = Required(Kelas)
    hari = Required(str)
    jam_mulai = Required(str)
    jam_selesai = Required(str)
    tahun_ajaran = Required(str)

    def to_dict(self):
        return {
            "id": self.id,
            "guru": self.pegawai.nama,
            "guru_id": self.pegawai.id,
            "mapel": self.mapel.nama,
            "mapel_id": self.mapel.id,
            "kelas": self.kelas.nama_kelas,
            "kelas_id": self.kelas.id,
            "hari": self.hari,
            "jam_mulai": self.jam_mulai,
            "jam_selesai": self.jam_selesai,
            "tahun_ajaran": self.tahun_ajaran
        }
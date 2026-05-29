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


class InformasiLembaga(db.Entity):
    judul = Required(str)
    isi = Required(str)
    tanggal = Optional(date)


class Surat(db.Entity):
    noSurat = Required(str)
    judul = Required(str)
    tanggal = Required(str) # Disimpan sebagai string sesuai input HTML5 date frontend "YYYY-MM-DD"
    jenis = Required(str)   # Masuk / Keluar
    deskripsi = Optional(str)

class Indikator(db.Entity):
    nama = Required(str)
    tipe = Required(str)    # angka / teks
    jenis = Required(str)   # Guru / Staff
    bobot = Required(int)
    urutan = Optional(int, default=1)
    relasi = Optional(str, default="Absen Masuk")
    status = Required(str, default="Aktif")


class KelolaKegiatan(db.Entity):
    _table_ = 'kelola_kegiatan'  # Nama tabel di database

    nama = Required(str)  # Menampung string nama kegiatan
    jenis = Required(str)  # Menampung string jenis kegiatan

    # Menggunakan str atau Optional(str) agar format datetime-local ("YYYY-MM-DDTHH:MM")
    # dari Frontend dapat langsung disimpan tanpa perlu parsing manual ke objek datetime.
    mulai = Required(str)
    selesai = Required(str)

    lokasi = Required(str)  # Menampung string lokasi kegiatan
    penanggungjawab = Required(str)  # Menampung string penanggung jawab (pj)

    status = Optional(str, default="Aktif")


class Cuti(db.Entity):
    _table_ = 'cuti'
    id = PrimaryKey(int, auto=True)
    nama = Required(str)                               # Nama Pegawai (dari select option)
    unit = Optional(str, default="0", nullable=True)   # Default "0" sesuai dengan FE payload
    mulai = Required(date)                             # Tanggal Mulai Cuti (Tipe Datetime/Date)
    selesai = Required(date)                           # Tanggal Selesai Cuti (Tipe Datetime/Date)
    alasan = Required(str)                             # Alasan Cuti (dari textarea)
    status = Required(str, default="Pending")          # Status: 'Pending', 'Approved', a


class Lembur(db.Entity):
    _table_ = 'lembur'
    id = PrimaryKey(int, auto=True)
    nama = Required(str)
    unit = Optional(str, default="0")
    mulai = Required(date)
    selesai = Required(date)
    alasan = Required(str)  # Bisa menggunakan str atau untuk teks panjang gunakan LongStr
    status = Required(str, default="Pending")

class Izin(db.Entity):
    _table_ = 'izin'
    id = PrimaryKey(int, auto=True)
    nama = Required(str)
    unit = Required(str, default="0")
    mulai = Required(date)
    selesai = Required(date)
    alasan = Required(str)
    status = Required(str, default="Pending")


class KomponenGaji(db.Entity):
    _table_ = 'komponen_gaji'  # Menentukan nama tabel di database

    id = PrimaryKey(int, auto=True)  # Menggunakan auto-increment jika FE tidak mengirim ID kustom
    nama = Required(str)
    jenis = Required(str)
    perhitungan = Required(str)
    nominal = Required(str)
    keterangan = Optional(str)

class RekapPresensi(db.Entity):
    id = PrimaryKey(int, auto=True)
    tanggal = Required(str)
    nip = Required(str)
    nama = Required(str)
    jenis_pegawai = Required(str)
    unit = Optional(str, default="0")
    jam_masuk = Optional(str)
    status_masuk = Optional(str)
    jam_pulang = Optional(str)
    status_pulang = Optional(str)
    keterangan = Required(str)
    terlambat = Optional(str)
    pulang_awal = Optional(str)
class PeriodeTanggal(db.Entity):
    _table_ = 'periode_tanggal'
    id = PrimaryKey(int, auto=True) # atau menggunakan tipe int besar jika id dikirim manual dari FE
    tanggal = Required(int, unique=True) # Menyimpan angka tanggal 1 - 31
    status = Required(str, default='Aktif')

class KriteriaKehadiran(db.Entity):
    _table_ = "kriteria_kehadiran"
    id = PrimaryKey(int, auto=True)
    nama = Required(str)
    kategori = Required(str)
    potongan = Required(bool, default=False)
    tunjangan = Required(bool, default=False)
    range = Required(bool, default=False)

class JenisPenerimaan(db.Entity):
    _table_ = "jenis_penerimaan"
    id = PrimaryKey(int, auto=True)
    akun_harta = Required(str)          # Contoh: "1.0.1 - Kas"
    jenis = Required(str)               # Contoh: "Dengan Pembatasan" / "Tanpa Pembatasan"
    akun_pendapatan = Required(str)     # Contoh: "4.0.4 Pendapatan Bos"
    keterangan = Optional(str, default='')
    kode_akun_penerimaan = Required(str)# Contoh: "4.0.4" atau "3"
    nama_akun_penerimaan = Required(str)# Contoh: "Pendapatan BOSDA"
    status = Required(str)


# ==========================================
# 2. ENTITAS SETTING GAJI KEHADIRAN
# ==========================================
class SettingGajiKehadiran(db.Entity):
    _table_ = "setting_gaji_kehadiran"
    id = PrimaryKey(int, auto=True)
    kriteria = Required(str)
    durasi = Required(str)
    jenis = Required(str)
    satuan = Required(str)
    nominal = Required(str)
    keterangan = Optional(str, default="")


class TransaksiPenerimaan(db.Entity):
    _table_ = "transaksi_penerimaan"
    id = PrimaryKey(int, auto=True)
    jenis = Required(str)          # SPP, Donasi, BOS
    nominal = Required(int)        # Pastikan Integer
    sumber = Required(str)
    menyetujui = Required(str)
    tanggal = Required(date)       # Pastikan tipe Date
    keterangan = Optional(str)
class Banner(db.Entity):
    _table_ = "banner_aplikasi"

    id = PrimaryKey(int, auto=True)

    nama = Required(str)
    tanggal = Required(datetime, default=datetime.now)
    gambar = Required(str)

    def to_dict(self):
        return {
            "id": self.id,
            "nama": self.nama,
            "tanggal": self.tanggal.strftime("%Y-%m-%d %H:%M:%S"),
            "gambar": self.gambar
        }

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


class AbsensiGPS(db.Entity):
    _table_ = "absensi_gps"

    id = PrimaryKey(int, auto=True)
    nama = Required(str)
    latitude = Required(str)
    longitude = Required(str)
    radius = Required(str)
    masuk = Required(str)  # Format string "HH:MM" dari frontend
    selesai = Required(str)  # Format string "HH:MM" dari frontend

    def to_dict(self):
        return {
            "id": self.id,
            "nama": self.nama,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "radius": self.radius,
            "masuk": self.masuk,
            "selesai": self.selesai
        }

# ==========================================
# BACKUP SYSTEM
# ==========================================
class BackupFile(db.Entity):
    _table_ = "backup_file"

    id = PrimaryKey(int, auto=True)
    nama = Required(str, unique=True)
    ukuran = Required(str)
    # Digabung menjadi satu objek datetime sesuai instruksi terbaru
    waktu_backup = Required(datetime, default=datetime.now)

    def to_dict(self):
        # Array pemetaan bulan Indonesia untuk kebutuhan output frontend
        bulan_indo = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agt", "Sep", "Okt", "Nov", "Des"]

        return {
            "id": self.id,
            "nama": self.nama,
            "ukuran": self.ukuran,
            # Memecah datetime menjadi format tanggal dan waktu terpisah untuk UI React Anda
            "tanggal": f"{self.waktu_backup.day:02d} {bulan_indo[self.waktu_backup.month - 1]} {self.waktu_backup.year}",
            "waktu": self.waktu_backup.strftime("%H:%M:%S")
        }
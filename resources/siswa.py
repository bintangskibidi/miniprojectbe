import falcon
from pony.orm import db_session, select
from models.schema import Siswa
from datetime import datetime


class SiswaResource:

    @db_session
    def on_get(self, req, resp):
        search = req.get_param("search")
        kelas = req.get_param("kelas")

        query = select(s for s in Siswa)

        if search:
            keyword = search.lower()
            query = query.filter(
                lambda s:
                    keyword in s.nama.lower() or
                    keyword in s.nis.lower()
            )

        if kelas:
            query = query.filter(lambda s: s.kelas == kelas)

        data = []

        for s in query:
            data.append({
                "id": s.id,
                "nis": s.nis,
                "nisn": s.nisn,
                "nama": s.nama,
                "kelas": s.kelas,
                "jurusan": s.jurusan,
                "status": s.status,
                "alamat": s.alamat
            })

        resp.media = {
            "status": True,
            "data": data
        }

    @db_session
    def on_post(self, req, resp):
        body = req.media

        tanggal = None
        if body.get("tanggal_lahir"):
            tanggal = datetime.strptime(
                body["tanggal_lahir"],
                "%Y-%m-%d"
            ).date()

        siswa = Siswa(
            nis=body.get("nis"),
            nisn=body.get("nisn"),
            nama=body.get("nama"),
            tempat_lahir=body.get("tempat_lahir"),
            tanggal_lahir=tanggal,
            jenis_kelamin=body.get("jenis_kelamin"),
            alamat=body.get("alamat"),
            agama=body.get("agama"),
            golongan_darah=body.get("golongan_darah"),

            status=body.get("status"),
            tahun_ajaran=body.get("tahun_ajaran"),
            tahun_masuk=body.get("tahun_masuk"),
            kelas=body.get("kelas"),
            jurusan=body.get("jurusan"),
            hp=body.get("hp"),
            sekolah_asal=body.get("sekolah_asal"),

            ayah=body.get("ayah"),
            ibu=body.get("ibu"),
            wali=body.get("wali"),

            pekerjaan_ayah=body.get("pekerjaan_ayah"),
            pekerjaan_ibu=body.get("pekerjaan_ibu"),

            hp_ayah=body.get("hp_ayah"),
            hp_ibu=body.get("hp_ibu"),
            hp_wali=body.get("hp_wali"),

            hubungan_wali=body.get("hubungan_wali")
        )

        resp.media = {
            "status": True,
            "message": "Data siswa berhasil ditambahkan",
            "id": siswa.id
        }


class DetailSiswaResource:

    @db_session
    def on_get(self, req, resp, id):
        siswa = Siswa.get(id=id)
        if not siswa:
            raise falcon.HTTPNotFound()
        resp.media = {
            "status": True,
            "data": siswa.to_dict()
        }

    @db_session
    def on_put(self, req, resp, id):
        # Ambil data dari request
        data = req.media
        
        # Cari data siswa berdasarkan ID
        siswa = Siswa.get(id=id)
        
        if not siswa:
            resp.status = falcon.HTTP_404
            resp.media = {"status": False, "message": "Siswa tidak ditemukan"}
            return

        # Proses Tanggal Lahir (Opsional: tambahkan logic strptime jika perlu)
        tgl_input = data.get('tanggal_lahir')
        tgl_final = None
        if tgl_input:
            try:
                # Mengubah string 'YYYY-MM-DD' menjadi objek date Python
                tgl_final = datetime.strptime(tgl_input, "%Y-%m-%d").date()
            except:
                tgl_final = None

        siswa.set(
            nis=data.get('nis') or "",
            nisn=data.get('nisn') or "",
            nama=data.get('nama') or "",
            tempat_lahir=data.get('tempat_lahir') or "",
            tanggal_lahir=tgl_final, 
            jenis_kelamin=data.get('jenis_kelamin') or "",
            alamat=data.get('alamat') or "", 
            agama=data.get('agama') or "",
            golongan_darah=data.get('golongan_darah') or "",
            status=data.get('status') or "Aktif",
            tahun_ajaran=data.get('tahun_ajaran') or "",
            tahun_masuk=data.get('tahun_masuk') or "",
            kelas=data.get('kelas') or "",
            jurusan=data.get('jurusan') or "",
            hp=data.get('hp') or "",
            sekolah_asal=data.get('sekolah_asal') or "",
            ayah=data.get('ayah') or "",
            ibu=data.get('ibu') or "",
            wali=data.get('wali') or "",
            pekerjaan_ayah=data.get('pekerjaan_ayah') or "",
            pekerjaan_ibu=data.get('pekerjaan_ibu') or "",
            hp_ayah=data.get('hp_ayah') or "",
            hp_ibu=data.get('hp_ibu') or "",
            hp_wali=data.get('hp_wali') or "",
            hubungan_wali=data.get('hubungan_wali') or ""
        )
        
        resp.media = {"status": True, "message": "Data berhasil diupdate"}

    @db_session
    def on_delete(self, req, resp, id):
        siswa = Siswa.get(id=id)
        if not siswa:
            raise falcon.HTTPNotFound()
        siswa.delete()
        resp.media = {
            "status": True,
            "message": "Data siswa berhasil dihapus"
        }

        
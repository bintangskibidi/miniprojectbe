import falcon
from pony.orm import db_session, select, commit
from models.schema import Presensi, Siswa, Kelas

class PresensiResource:
    @db_session
    def on_get(self, req, resp, id=None):
        if id:
            try:
                p = Presensi[int(id)]
                resp.media = {"status": True, "data": p.to_dict()}
            except:
                resp.status = falcon.HTTP_404
        else:
            data = []
            presensi_list = select(p for p in Presensi)[:]
            for p in presensi_list:
                d = p.to_dict()
                d['nama'] = p.siswa.nama
                d['nis'] = p.siswa.nis
                d['nama_kelas'] = p.kelas.nama_kelas
                data.append(d)
            resp.media = {"status": True, "data": data}

    @db_session
    def on_post(self, req, resp):
        data = req.media
        try:
            siswa_obj = Siswa.get(id=data.get('id_siswa'))
            if not siswa_obj:
                resp.status = falcon.HTTP_400
                resp.media = {"status": False, "message": "Siswa tidak ditemukan"}
                return

            # Cari kelas (berdasarkan nama atau kode)
            kelas_input = data.get('kelas')
            kelas_obj = Kelas.get(nama_kelas=kelas_input) or Kelas.get(kode_kelas=kelas_input)

            if not kelas_obj:
                resp.status = falcon.HTTP_400
                resp.media = {"status": False, "message": "Kelas tidak ditemukan"}
                return

            existing = Presensi.get(siswa=siswa_obj, tanggal=data.get('tanggal'))

            if existing:
                incoming_keterangan = data.get("keterangan")
                jam_pulang_baru = data.get("jamPulang")

                # 1. Update Ijin/Sakit
                if incoming_keterangan in ["Ijin", "Sakit"]:
                    existing.set(
                        keterangan=incoming_keterangan,
                        detail_ijin=data.get("detailIjin", ""),
                        jam_masuk="-", jam_pulang="-", status_masuk="-"
                    )
                    commit() # Simpan perubahan
                    resp.media = {"status": True, "data": existing.to_dict(), "message": "Ijin disimpan"}
                    return

                # 2. Update Jam Pulang
                if jam_pulang_baru and jam_pulang_baru != "-":
                    if existing.jam_pulang != "-":
                        resp.status = falcon.HTTP_400
                        resp.media = {"status": False, "message": "Sudah absen pulang"}
                        return
                    existing.set(jam_pulang=jam_pulang_baru)
                    commit()
                    resp.media = {"status": True, "data": existing.to_dict(), "message": "Absen pulang berhasil"}
                    return

                # 3. Cek jika sudah masuk
                if existing.jam_masuk != "-":
                    resp.status = falcon.HTTP_400
                    resp.media = {"status": False, "message": "Sudah absen masuk hari ini"}
                    return

            # SIMPAN DATA BARU
            new_p = Presensi(
                siswa=siswa_obj,
                kelas=kelas_obj,
                tanggal=data.get('tanggal'),
                jam_masuk=data.get('jamMasuk', '-'),
                jam_pulang=data.get('jamPulang', '-'),
                status_masuk=data.get('statusMasuk', '-'),
                keterangan=data.get('keterangan', 'Hadir'),
                detail_ijin=data.get('detailIjin', '')
            )
            commit() # WAJIB agar ID ter-generate

            # Balikkan data lengkap (termasuk ID) ke FE
            resp.media = {
                "status": True,
                "message": "Presensi berhasil disimpan",
                "data": new_p.to_dict()
            }

        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": False, "message": str(e)}

    @db_session
    def on_put(self, req, resp, id):
        data = req.media
        try:
            # Cast ID ke Integer agar Pony ORM tidak bingung
            k = Presensi[int(id)]
            k.set(**data)
            resp.media = {"status": True, "message": "Data berhasil diubah"}
        except Exception as e:
            resp.status = falcon.HTTP_404
            resp.media = {"status": False, "message": "Data tidak ditemukan"}

    @db_session
    def on_delete(self, req, resp, id):
        try:
            k = Presensi[int(id)]
            k.delete()
            resp.media = {"status": True, "message": "Data dihapus"}
        except:
            resp.status = falcon.HTTP_404
            resp.media = {"status": False, "message": "Gagal hapus"}
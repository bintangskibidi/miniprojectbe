import falcon
from pony.orm import db_session, select
from models.schema import JadwalMengajar, Pegawai, Mapel, Kelas


class JadwalMengajarResource:

    # ================= GET =================
    @db_session
    def on_get(self, req, resp):
        tahun_ajaran = req.get_param("tahun_ajaran")

        query = select(j for j in JadwalMengajar)

        if tahun_ajaran:
            query = select(
                j for j in JadwalMengajar
                if j.tahun_ajaran == tahun_ajaran
            )

        data = []
        for j in query:
            data.append({
                "id": j.id,

                "guru": j.pegawai.nama,        # ✅ FIX
                "guru_id": j.pegawai.id,       # ✅ FIX

                "mapel": j.mapel.nama,
                "mapel_id": j.mapel.id,

                "kelas": j.kelas.nama_kelas,
                "kelas_id": j.kelas.id,

                "hari": j.hari,
                "jam_mulai": j.jam_mulai,
                "jam_selesai": j.jam_selesai,
                "jam": f"{j.jam_mulai} - {j.jam_selesai}",

                "tahun_ajaran": j.tahun_ajaran
            })

        resp.media = {
            "status": True,
            "data": data
        }

    # ================= CREATE =================
    @db_session
    def on_post(self, req, resp):
        data = req.media

        JadwalMengajar(
            pegawai=Pegawai[data["guru_id"]],   # ✅ FIX (bukan Guru)
            mapel=Mapel[data["mapel_id"]],
            kelas=Kelas[data["kelas_id"]],
            hari=data["hari"],
            jam_mulai=data["jam_mulai"],
            jam_selesai=data["jam_selesai"],
            tahun_ajaran=data["tahun_ajaran"]
        )

        resp.media = {
            "status": True,
            "message": "Jadwal berhasil ditambahkan"
        }

    # ================= UPDATE =================
    @db_session
    def on_put(self, req, resp, id):
        jadwal = JadwalMengajar.get(id=id)

        if not jadwal:
            raise falcon.HTTPNotFound()

        data = req.media

        jadwal.pegawai = Pegawai[data["guru_id"]]   # ✅ FIX
        jadwal.mapel = Mapel[data["mapel_id"]]
        jadwal.kelas = Kelas[data["kelas_id"]]
        jadwal.hari = data["hari"]
        jadwal.jam_mulai = data["jam_mulai"]
        jadwal.jam_selesai = data["jam_selesai"]

        resp.media = {
            "status": True,
            "message": "Jadwal berhasil diupdate"
        }

    # ================= DELETE =================
    @db_session
    def on_delete(self, req, resp, id):
        jadwal = JadwalMengajar.get(id=id)

        if not jadwal:
            raise falcon.HTTPNotFound()

        jadwal.delete()

        resp.media = {
            "status": True,
            "message": "Jadwal berhasil dihapus"
        }


# ================= DROPDOWN =================
class JadwalDropdownResource:

    @db_session
    def on_get(self, req, resp):
        resp.media = {
            "status": True,
            "data": {
                "guru": [
                    {
                        "id": p.id,
                        "nama": p.nama
                    }
                    for p in select(p for p in Pegawai)
                ],

                "mapel": [
                    {
                        "id": m.id,
                        "nama": m.nama
                    }
                    for m in select(m for m in Mapel)
                ],

                "kelas": [
                    {
                        "id": k.id,
                        "nama": k.nama_kelas
                    }
                    for k in select(k for k in Kelas)
                ]
            }
        }
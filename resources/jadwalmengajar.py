import falcon
from pony.orm import db_session, select
# Pastiin import-nya Pegawai, karena di schema lu namanya itu
from models.schema import JadwalMengajar, Pegawai, Mapel, Kelas


class JadwalMengajarResource:

    # ================= GET =================
    @db_session
    def on_get(self, req, resp):
        tahun_ajaran = req.get_param("tahun_ajaran")
        query = select(j for j in JadwalMengajar)

        if tahun_ajaran:
            query = select(j for j in JadwalMengajar if j.tahun_ajaran == tahun_ajaran)

        data = []
        for j in query:
            data.append({
                "id": j.id,
                # Di schema lu field-nya namanya 'pegawai'
                "guru": j.pegawai.nama,
                "guru_id": j.pegawai.id,

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

        resp.media = {"status": True, "data": data}

    # ================= CREATE =================
    @db_session
    def on_post(self, req, resp):
        data = req.media

        # Pake .get() biar kaga crash kalo FE ngirim ID gaib
        pegawai = Pegawai.get(id=data.get("guru_id"))
        mapel = Mapel.get(id=data.get("mapel_id"))
        kelas = Kelas.get(id=data.get("kelas_id"))

        if not all([pegawai, mapel, kelas]):
            resp.status = falcon.HTTP_400
            resp.media = {"status": False, "message": "Data Pegawai, Mapel, atau Kelas kaga ketemu!"}
            return

        JadwalMengajar(
            pegawai=pegawai,
            mapel=mapel,
            kelas=kelas,
            hari=data.get("hari"),
            jam_mulai=data.get("jam_mulai"),
            jam_selesai=data.get("jam_selesai"),
            tahun_ajaran=data.get("tahun_ajaran")
        )

        resp.media = {"status": True, "message": "Jadwal berhasil ditambahkan"}

    # ================= UPDATE =================
    @db_session
    def on_put(self, req, resp, id):
        jadwal = JadwalMengajar.get(id=id)
        if not jadwal:
            raise falcon.HTTPNotFound()

        data = req.media
        p = Pegawai.get(id=data.get("guru_id"))
        m = Mapel.get(id=data.get("mapel_id"))
        k = Kelas.get(id=data.get("kelas_id"))

        if not all([p, m, k]):
            resp.status = falcon.HTTP_400
            resp.media = {"status": False, "message": "Update gagal, ID relasi kaga valid"}
            return

        jadwal.pegawai = p
        jadwal.mapel = m
        jadwal.kelas = k
        jadwal.hari = data.get("hari")
        jadwal.jam_mulai = data.get("jam_mulai")
        jadwal.jam_selesai = data.get("jam_selesai")

        resp.media = {"status": True, "message": "Jadwal berhasil diupdate"}

    # ================= DELETE =================
    @db_session
    def on_delete(self, req, resp, id):
        jadwal = JadwalMengajar.get(id=id)
        if not jadwal:
            raise falcon.HTTPNotFound()
        jadwal.delete()
        resp.media = {"status": True, "message": "Jadwal berhasil dihapus"}


# ================= DROPDOWN =================
class JadwalDropdownResource:
    @db_session
    def on_get(self, req, resp):
        resp.media = {
            "status": True,
            "data": {
                "guru": [{"id": p.id, "nama": p.nama} for p in select(p for p in Pegawai)],
                "mapel": [{"id": m.id, "nama": m.nama} for m in select(m for m in Mapel)],
                "kelas": [{"id": k.id, "nama": k.nama_kelas} for k in select(k for k in Kelas)]
            }
        }
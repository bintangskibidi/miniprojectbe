from pony.orm import db_session, select
from models.schema import JadwalMengajar
import falcon


class RiwayatMengajarResource:

    @db_session
    def on_get(self, req, resp):

        tahun = req.get_param("tahun")
        guru = req.get_param("guru")
        kelas = req.get_param("kelas")

        query = select(j for j in JadwalMengajar)

        if tahun:
            query = query.filter(
                lambda j: j.tahun_ajaran == tahun
            )

        if guru:
            query = query.filter(
                lambda j: guru.lower() in j.guru.nama.lower()
            )

        if kelas:
            query = query.filter(
                lambda j: kelas.lower() in j.kelas.nama.lower()
            )

        data = []

        for item in query:
            data.append({
                "id": item.id,
                "tanggal": "-",  # nanti isi kalau ada field tanggal
                "jam": f"{item.jam_mulai} - {item.jam_selesai}",
                "mapel": item.mapel.nama if item.mapel else "-",
                "guru": item.guru.nama if item.guru else "-",
                "kelas": item.kelas.nama if item.kelas else "-",
                "siswa": "-",
                "status": "Hadir",
                "keterangan": "-",
                "waktu_absen": "-"
            })

        resp.media = {
            "success": True,
            "data": data
        }
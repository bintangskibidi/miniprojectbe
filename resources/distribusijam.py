from pony.orm import db_session, select
from models.schema import JadwalMengajar


class DistribusiJamResource:

    @db_session
    def on_get(self, req, resp):

        tahun_ajaran = req.get_param("tahun_ajaran")

        query = select(j for j in JadwalMengajar)

        if tahun_ajaran:
            query = select(
                j for j in JadwalMengajar
                if j.tahun_ajaran == tahun_ajaran
            )

        hasil = {}

        for j in query:

            nama_guru = j.pegawai.nama

            # convert jam ke menit
            mulai_jam, mulai_menit = map(int, j.jam_mulai.split(":"))
            selesai_jam, selesai_menit = map(int, j.jam_selesai.split(":"))

            total_mulai = (mulai_jam * 60) + mulai_menit
            total_selesai = (selesai_jam * 60) + selesai_menit

            durasi = total_selesai - total_mulai

            if nama_guru not in hasil:
                hasil[nama_guru] = 0

            hasil[nama_guru] += durasi

        data = []

        for nama, total_menit in hasil.items():

            jam = total_menit // 60
            menit = total_menit % 60

            data.append({
                "nama": nama,
                "jam": jam,
                "menit": menit,
                "total_menit": total_menit
            })

        # urut terbesar
        data.sort(key=lambda x: x["total_menit"], reverse=True)

        resp.media = {
            "status": True,
            "data": data
        }
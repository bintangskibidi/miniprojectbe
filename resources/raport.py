import falcon
from pony.orm import db_session, select
from models.schema import (
    Raport,
    Siswa,
    Kelas,
    Semester,
    AspekPenilaian,
    TahunAjaran,
    Pegawai
)


class RaportResource:

    # =========================
    # GET DATA RAPORT
    # =========================
    @db_session
    def on_get(self, req, resp):
        kelas_id = req.get_param("kelas_id")
        semester_id = req.get_param("semester_id")
        mapel_id = req.get_param("mapel_id")

        if not kelas_id or not semester_id or not mapel_id:
            resp.media = []
            return

        data = select(r for r in Raport if
            r.kelas.id == int(kelas_id) and
            r.semester.id == int(semester_id) and
            r.mapel.id == int(mapel_id)
        )[:]

        result = []

        for r in data:
            result.append({
                "id": r.id,
                "siswa_id": r.siswa.id,
                "kkm": r.kkm,
                "harian": r.harian,
                "ujian": r.ujian,
                "deskripsi": r.deskripsi
            })

        resp.media = result

    # =========================
    # AUTO SAVE RAPORT
    # =========================
    @db_session
    def on_post(self, req, resp):
        data = req.media

        siswa_id = int(data.get("siswa_id"))
        kelas_id = int(data.get("kelas_id"))
        semester_id = int(data.get("semester_id"))
        mapel_id = int(data.get("mapel_id"))

        tahun_id = data.get("tahun_ajaran_id")
        wali_id = data.get("wali_id")

        # relasi
        siswa = Siswa.get(id=siswa_id)
        kelas = Kelas.get(id=kelas_id)
        semester = Semester.get(id=semester_id)
        mapel = AspekPenilaian.get(id=mapel_id)

        tahun = TahunAjaran.get(id=tahun_id) if tahun_id else None
        wali = Pegawai.get(id=wali_id) if wali_id else None

        # cek existing
        raport = Raport.get(
            siswa=siswa,
            kelas=kelas,
            semester=semester,
            mapel=mapel
        )

        # create baru jika belum ada
        if not raport:
            raport = Raport(
                siswa=siswa,
                kelas=kelas,
                semester=semester,
                mapel=mapel
            )

        # update data
        raport.kkm = data.get("kkm")
        raport.harian = data.get("harian")
        raport.ujian = data.get("ujian")
        raport.deskripsi = data.get("deskripsi")

        if tahun:
            raport.tahun_ajaran = tahun

        if wali:
            raport.wali = wali

        resp.media = {
            "status": True,
            "message": "Raport saved",
            "siswa_id": siswa_id
        }
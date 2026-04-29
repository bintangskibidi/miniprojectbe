from pony.orm import db_session, select
import falcon
from models.schema import Semester, TahunAjaran, JenisSemester


class SemesterResource:
    @db_session
    def on_get(self, req, resp, id=None):
        if req.get_param("dropdown") == "true":
            data = [
                {
                    "id": s.id,
                    "nama_semester": s.nama_semester,
                    "tahun_ajaran_id": s.tahun_ajaran.id,
                    "tahun_ajaran": s.tahun_ajaran.tahun_ajaran,
                    "jenis_semester_id": s.jenis_semester.id,
                    "jenis_semester": s.jenis_semester.nama,
                }
                for s in select(s for s in Semester)
            ]

            resp.status = falcon.HTTP_200
            resp.media = {
                "success": True,
                "message": "Data semester dropdown berhasil diambil",
                "data": data,
            }
            return

        if id:
            semester = Semester.get(id=id)
            if not semester:
                resp.status = falcon.HTTP_404
                resp.media = {
                    "success": False,
                    "message": "Data semester tidak ditemukan",
                }
                return

            resp.media = {
                "success": True,
                "data": semester.to_dict(),
            }
            return

        semesters = select(s for s in Semester)[:]
        resp.media = {
            "success": True,
            "data": [s.to_dict() for s in semesters],
        }

    @db_session
    def on_post(self, req, resp):
        data = req.media

        semester = Semester(
            tahun_ajaran=TahunAjaran[data["tahun_ajaran_id"]],
            jenis_semester=JenisSemester[data["jenis_semester_id"]],
            nama_semester=data["nama_semester"],
        )

        resp.status = falcon.HTTP_201
        resp.media = {
            "success": True,
            "message": "Data semester berhasil ditambahkan",
            "data": semester.to_dict(),
        }

    @db_session
    def on_put(self, req, resp, id):
        semester = Semester.get(id=id)

        if not semester:
            resp.status = falcon.HTTP_404
            resp.media = {
                "success": False,
                "message": "Data semester tidak ditemukan",
            }
            return

        data = req.media

        semester.tahun_ajaran = TahunAjaran[data["tahun_ajaran_id"]]
        semester.jenis_semester = JenisSemester[data["jenis_semester_id"]]
        semester.nama_semester = data["nama_semester"]

        resp.media = {
            "success": True,
            "message": "Data semester berhasil diupdate",
            "data": semester.to_dict(),
        }

    @db_session
    def on_delete(self, req, resp, id):
        semester = Semester.get(id=id)

        if not semester:
            resp.status = falcon.HTTP_404
            resp.media = {
                "success": False,
                "message": "Data semester tidak ditemukan",
            }
            return

        semester.delete()

        resp.media = {
            "success": True,
            "message": "Data semester berhasil dihapus",
        }
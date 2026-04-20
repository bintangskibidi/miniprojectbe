import falcon
from pony.orm import commit, db_session, select
from models.schema import Siswa


class SiswaResource:

    @db_session
    def on_get(self, req, resp):
        search = req.get_param("search")
        kelas = req.get_param("kelas")

        query = select(s for s in Siswa)

        if search:
            query = query.filter(
                lambda s: search.lower() in s.nama.lower()
                or search.lower() in s.nis.lower()
            )

        if kelas:
            query = query.filter(lambda s: s.kelas == kelas)

        data = []

        for s in query:
            data.append({
                "id": s.id,
                "nis": s.nis,
                "nama": s.nama,
                "kelas": s.kelas,
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

        siswa = Siswa(
            nis=body.get("nis"),
            nama=body.get("nama"),
            kelas=body.get("kelas"),
            status=body.get("status"),
            alamat=body.get("alamat")
        )
        commit()

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
        siswa = Siswa.get(id=id)

        if not siswa:
            raise falcon.HTTPNotFound()

        body = req.media

        siswa.set(
            nis=body.get("nis"),
            nama=body.get("nama"),
            kelas=body.get("kelas"),
            status=body.get("status"),
            alamat=body.get("alamat")
        )

        resp.media = {
            "status": True,
            "message": "Data siswa berhasil diupdate"
        }

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
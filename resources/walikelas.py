import falcon
from pony.orm import db_session
from models.schema import WaliKelas
import json


class WaliKelasResource:

    @db_session
    def on_get(self, req, resp):
        query = WaliKelas.select()

        data = [
            {
                "id": w.id,
                "namaKelas": w.nama_kelas,
                "namaPegawai": w.nama_pegawai,
                "tahunAjaran": w.tahun_ajaran
            }
            for w in query
        ]

        resp.media = {
            "status": True,
            "data": data
        }

    @db_session
    def on_post(self, req, resp):
        body = self._get_json(req)

        if not body:
            resp.status = falcon.HTTP_400
            resp.media = {"status": False, "message": "JSON kosong / tidak valid"}
            return

        if not body.get("namaKelas") or not body.get("namaPegawai") or not body.get("tahunAjaran"):
            resp.status = falcon.HTTP_400
            resp.media = {"status": False, "message": "Data tidak lengkap"}
            return

        baru = WaliKelas(
            nama_kelas=body["namaKelas"],
            nama_pegawai=body["namaPegawai"],
            tahun_ajaran=body["tahunAjaran"]
        )

        resp.status = falcon.HTTP_201
        resp.media = {
            "status": True,
            "message": "Data berhasil ditambahkan",
            "id": baru.id
        }

    def _get_json(self, req):
        """Helper biar POST & PUT konsisten"""
        try:
            if req.media:
                return req.media
        except Exception:
            pass

        try:
            raw = req.stream.read(req.content_length or 0)
            if raw:
                return json.loads(raw)
        except Exception:
            return None

        return None


class DetailwalikelasResource:

    @db_session
    def on_get(self, req, resp, id):
        try:
            item = WaliKelas.get(id=int(id))
        except ValueError:
            item = None

        if not item:
            resp.status = falcon.HTTP_404
            resp.media = {"status": False, "message": "Data tidak ditemukan"}
            return

        resp.media = {
            "status": True,
            "data": {
                "id": item.id,
                "namaKelas": item.nama_kelas,
                "namaPegawai": item.nama_pegawai,
                "tahunAjaran": item.tahun_ajaran
            }
        }

    @db_session
    def on_put(self, req, resp, id):
        body = self._get_json(req)

        if not body:
            resp.status = falcon.HTTP_400
            resp.media = {"status": False, "message": "JSON kosong / tidak valid"}
            return

        item = WaliKelas.get(id=int(id))

        if not item:
            resp.status = falcon.HTTP_404
            resp.media = {"status": False, "message": "Data tidak ditemukan"}
            return

        item.set(
            nama_kelas=body.get('namaKelas', item.nama_kelas),
            nama_pegawai=body.get('namaPegawai', item.nama_pegawai),
            tahun_ajaran=body.get('tahunAjaran', item.tahun_ajaran)
        )

        resp.media = {
            "status": True,
            "message": "Data berhasil diupdate"
        }

    @db_session
    def on_delete(self, req, resp, id):
        item = WaliKelas.get(id=int(id))

        if not item:
            resp.status = falcon.HTTP_404
            resp.media = {"status": False, "message": "Data tidak ditemukan"}
            return

        item.delete()

        resp.media = {
            "status": True,
            "message": "Data berhasil dihapus"
        }

    def _get_json(self, req):
        """Helper biar PUT juga aman"""
        try:
            if req.media:
                return req.media
        except Exception:
            pass

        try:
            raw = req.stream.read(req.content_length or 0)
            if raw:
                return json.loads(raw)
        except Exception:
            return None

        return None
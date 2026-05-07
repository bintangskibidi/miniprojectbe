import falcon
from pony.orm import db_session, select, commit
from models.schema import Pegawai
from datetime import date


class PegawaiResource:

    # ================= GET =================
    @db_session
    def on_get(self, req, resp):
        data = [p.to_dict() for p in select(p for p in Pegawai)]

        resp.media = {
            "status": True,
            "data": data
        }

    # ================= CREATE =================
    @db_session
    def on_post(self, req, resp):
        data = req.media

        Pegawai(
            nama=data["nama"],
            nip=data.get("nip"),
            pendidikan=data.get("pendidikan"),
            golongan=data.get("golongan"),
            status_pegawai=data.get("status_pegawai"),
            tanggal_sk=data.get("tanggal_sk"),
            jabatan=data["jabatan"],
            no_hp=data.get("no_hp"),
            email=data.get("email"),
            jenis_pegawai=data.get("jenis_pegawai"),
            unit=data.get("unit"),
            status=data.get("status")
        )

        commit()

        resp.media = {
            "status": True,
            "message": "Pegawai berhasil ditambahkan"
        }

    # ================= UPDATE =================
    @db_session
    def on_put(self, req, resp, id):
        pegawai = Pegawai.get(id=id)

        if not pegawai:
            raise falcon.HTTPNotFound()

        data = req.media

        pegawai.nama = data["nama"]
        pegawai.nip = data.get("nip")
        pegawai.pendidikan = data.get("pendidikan")
        pegawai.golongan = data.get("golongan")
        pegawai.status_pegawai = data.get("status_pegawai")
        pegawai.tanggal_sk = data.get("tanggal_sk")
        pegawai.jabatan = data["jabatan"]
        pegawai.no_hp = data.get("no_hp")
        pegawai.email = data.get("email")
        pegawai.jenis_pegawai = data.get("jenis_pegawai")
        pegawai.unit = data.get("unit")
        pegawai.status = data.get("status")

        commit()

        resp.media = {
            "status": True,
            "message": "Pegawai berhasil diupdate"
        }

    # ================= DELETE =================
    @db_session
    def on_delete(self, req, resp, id):
        pegawai = Pegawai.get(id=id)

        if not pegawai:
            raise falcon.HTTPNotFound()

        pegawai.delete()
        commit()

        resp.media = {
            "status": True,
            "message": "Pegawai berhasil dihapus"
        }
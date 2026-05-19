from pony.orm import db_session, select, commit
import falcon
from models.schema import Pegawai


class PegawaiResource:

    # ================= GET =================
    @db_session
    def on_get(self, req, resp):

        try:
            data = [p.to_dict() for p in select(p for p in Pegawai)]

            resp.media = {
                "status": True,
                "data": data
            }

        except Exception as e:

            print("ERROR GET PEGAWAI:", e)

            resp.status = falcon.HTTP_400

            resp.media = {
                "status": False,
                "message": str(e)
            }

    # ================= CREATE =================
    @db_session
    def on_post(self, req, resp):

        try:
            data = req.media

            Pegawai(
                nama=data.get("nama"),
                nip=data.get("nip"),
                pendidikan=data.get("pendidikan"),
                golongan=data.get("golongan"),
                status_pegawai=data.get("status_pegawai"),

                # STRING BIASA
                tanggal_sk=data.get("tanggal_sk"),

                jabatan=data.get("jabatan"),
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

        except Exception as e:

            print("ERROR POST PEGAWAI:", e)

            resp.status = falcon.HTTP_400

            resp.media = {
                "status": False,
                "message": str(e)
            }

    # ================= UPDATE =================
    @db_session
    def on_put(self, req, resp, id):

        try:
            pegawai = Pegawai.get(id=id)

            if not pegawai:
                raise falcon.HTTPNotFound()

            data = req.media

            pegawai.nama = data.get("nama")
            pegawai.nip = data.get("nip")
            pegawai.pendidikan = data.get("pendidikan")
            pegawai.golongan = data.get("golongan")
            pegawai.status_pegawai = data.get("status_pegawai")

            # STRING BIASA
            pegawai.tanggal_sk = data.get("tanggal_sk")

            pegawai.jabatan = data.get("jabatan")
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

        except Exception as e:

            print("ERROR UPDATE PEGAWAI:", e)

            resp.status = falcon.HTTP_400

            resp.media = {
                "status": False,
                "message": str(e)
            }

    # ================= DELETE =================
    @db_session
    def on_delete(self, req, resp, id):

        try:
            pegawai = Pegawai.get(id=id)

            if not pegawai:
                raise falcon.HTTPNotFound()

            pegawai.delete()

            commit()

            resp.media = {
                "status": True,
                "message": "Pegawai berhasil dihapus"
            }

        except Exception as e:

            print("ERROR DELETE PEGAWAI:", e)

            resp.status = falcon.HTTP_400

            resp.media = {
                "status": False,
                "message": str(e)
            }
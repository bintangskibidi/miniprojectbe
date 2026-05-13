import falcon
from pony.orm import db_session, select, commit
from models.schema import Presensi, Siswa, Kelas


class PresensiResource:

    @db_session
    def on_get(self, req, resp, id=None):

        if id:
            try:
                p = Presensi[int(id)]

                data = p.to_dict()
                data["nama"] = p.siswa.nama
                data["nis"] = p.siswa.nis
                data["nama_kelas"] = p.kelas.nama_kelas

                resp.media = {
                    "status": True,
                    "data": data
                }

            except:
                resp.status = falcon.HTTP_404
                resp.media = {
                    "status": False,
                    "message": "Data tidak ditemukan"
                }

        else:
            data = []

            presensi_list = select(p for p in Presensi)[:]

            for p in presensi_list:
                d = p.to_dict()

                d["nama"] = p.siswa.nama
                d["nis"] = p.siswa.nis
                d["nama_kelas"] = p.kelas.nama_kelas

                data.append(d)

            resp.media = {
                "status": True,
                "data": data
            }

    @db_session
    def on_post(self, req, resp):

        data = req.media

        try:

            # =========================
            # VALIDASI SISWA
            # =========================
            siswa_obj = Siswa.get(id=data.get("id_siswa"))

            if not siswa_obj:
                resp.status = falcon.HTTP_400
                resp.media = {
                    "status": False,
                    "message": "Siswa tidak ditemukan"
                }
                return

            # =========================
            # VALIDASI KELAS
            # =========================
            kelas_input = data.get("kelas")

            kelas_obj = (
                Kelas.get(nama_kelas=kelas_input)
                or
                Kelas.get(kode_kelas=kelas_input)
            )

            if not kelas_obj:
                resp.status = falcon.HTTP_400
                resp.media = {
                    "status": False,
                    "message": "Kelas tidak ditemukan"
                }
                return

            tanggal = data.get("tanggal")

            existing = Presensi.get(
                siswa=siswa_obj,
                tanggal=tanggal
            )

            incoming_keterangan = data.get("keterangan")
            incoming_jam_masuk = data.get("jamMasuk")
            incoming_jam_pulang = data.get("jamPulang")

            # ==================================================
            # JIKA SUDAH ADA DATA HARI INI
            # ==================================================
            if existing:

                # ----------------------------------------------
                # STATUS SEKARANG
                # ----------------------------------------------
                sudah_pulang = (
                    existing.keterangan == "Pulang"
                    or
                    (
                        existing.jam_pulang
                        and
                        existing.jam_pulang != "-"
                    )
                )

                sudah_ijin = existing.keterangan in [
                    "Ijin",
                    "Sakit",
                    "Alfa"
                ]

                sudah_masuk = (
                    existing.jam_masuk
                    and
                    existing.jam_masuk != "-"
                )

                # ==================================================
                # JIKA SUDAH PULANG
                # ==================================================
                if sudah_pulang:
                    resp.status = falcon.HTTP_400
                    resp.media = {
                        "status": False,
                        "message": "Anda sudah absen pulang hari ini"
                    }
                    return

                # ==================================================
                # JIKA SUDAH IJIN / SAKIT / ALFA
                # ==================================================
                if sudah_ijin:
                    resp.status = falcon.HTTP_400
                    resp.media = {
                        "status": False,
                        "message": f"Anda sudah berstatus {existing.keterangan} hari ini"
                    }
                    return

                # ==================================================
                # REQUEST IJIN / SAKIT / ALFA
                # ==================================================
                if incoming_keterangan in ["Ijin", "Sakit", "Alfa"]:

                    # Kalau sudah masuk, masih boleh update jadi ijin
                    existing.set(
                        keterangan=incoming_keterangan,
                        detail_ijin=data.get("detailIjin", ""),
                        jam_masuk="-",
                        jam_pulang="-",
                        status_masuk="-"
                    )

                    commit()

                    resp.media = {
                        "status": True,
                        "message": f"{incoming_keterangan} berhasil disimpan",
                        "data": existing.to_dict()
                    }

                    return

                # ==================================================
                # ABSEN PULANG
                # ==================================================
                if incoming_jam_pulang and incoming_jam_pulang != "-":

                    # Harus sudah masuk
                    if not sudah_masuk:
                        resp.status = falcon.HTTP_400
                        resp.media = {
                            "status": False,
                            "message": "Belum absen masuk"
                        }
                        return

                    # Tidak boleh pulang 2x
                    if existing.jam_pulang != "-":
                        resp.status = falcon.HTTP_400
                        resp.media = {
                            "status": False,
                            "message": "Sudah absen pulang"
                        }
                        return

                    existing.set(
                        jam_pulang=incoming_jam_pulang,
                        keterangan="Pulang"
                    )

                    commit()

                    resp.media = {
                        "status": True,
                        "message": "Absen pulang berhasil",
                        "data": existing.to_dict()
                    }

                    return

                # ==================================================
                # ABSEN MASUK LAGI
                # ==================================================
                if incoming_jam_masuk and incoming_jam_masuk != "-":

                    if sudah_masuk:
                        resp.status = falcon.HTTP_400
                        resp.media = {
                            "status": False,
                            "message": "Sudah absen masuk hari ini"
                        }
                        return

            # ==================================================
            # SIMPAN DATA BARU
            # ==================================================
            new_p = Presensi(
                siswa=siswa_obj,
                kelas=kelas_obj,
                tanggal=tanggal,

                jam_masuk=data.get("jamMasuk", "-"),
                jam_pulang=data.get("jamPulang", "-"),

                status_masuk=data.get("statusMasuk", "-"),

                keterangan=data.get("keterangan", "Hadir"),

                detail_ijin=data.get("detailIjin", "")
            )

            commit()

            resp.media = {
                "status": True,
                "message": "Presensi berhasil disimpan",
                "data": new_p.to_dict()
            }

        except Exception as e:

            resp.status = falcon.HTTP_500

            resp.media = {
                "status": False,
                "message": str(e)
            }

    @db_session
    def on_put(self, req, resp, id):

        data = req.media

        try:

            p = Presensi[int(id)]

            # ==========================================
            # VALIDASI SUDAH PULANG
            # ==========================================
            if p.keterangan == "Pulang":
                resp.status = falcon.HTTP_400
                resp.media = {
                    "status": False,
                    "message": "Sudah absen pulang"
                }
                return

            # ==========================================
            # VALIDASI SUDAH IJIN
            # ==========================================
            if p.keterangan in ["Ijin", "Sakit", "Alfa"]:
                resp.status = falcon.HTTP_400
                resp.media = {
                    "status": False,
                    "message": f"Sudah berstatus {p.keterangan}"
                }
                return

            # ==========================================
            # UPDATE JAM PULANG
            # ==========================================
            if "jamPulang" in data:

                if p.jam_pulang != "-":
                    resp.status = falcon.HTTP_400
                    resp.media = {
                        "status": False,
                        "message": "Sudah absen pulang"
                    }
                    return

                p.jam_pulang = data["jamPulang"]
                p.keterangan = "Pulang"

            commit()

            resp.media = {
                "status": True,
                "message": "Data berhasil diubah",
                "data": p.to_dict()
            }

        except Exception as e:

            resp.status = falcon.HTTP_404

            resp.media = {
                "status": False,
                "message": str(e)
            }

    @db_session
    def on_delete(self, req, resp, id):

        try:

            p = Presensi[int(id)]

            p.delete()

            commit()

            resp.media = {
                "status": True,
                "message": "Data berhasil dihapus"
            }

        except:

            resp.status = falcon.HTTP_404

            resp.media = {
                "status": False,
                "message": "Gagal hapus data"
            }
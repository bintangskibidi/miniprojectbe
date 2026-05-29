import falcon
from pony.orm import db_session, select
from datetime import datetime
# Pastikan mengimpor model TransaksiPenerimaan yang benar
from models.schema import TransaksiPenerimaan


class TransaksiPenerimaanResource:
    @db_session
    def on_get(self, req, resp, id=None):
        """
        Mengambil satu data berdasarkan ID atau mengambil semua data transaksi.
        """
        if id:
            try:
                transaksi = TransaksiPenerimaan[id]
                resp.media = {"status": True, "data": transaksi.to_dict()}
            except Exception:
                resp.status = falcon.HTTP_404
                resp.media = {
                    "status": False,
                    "message": "Data transaksi penerimaan tidak ditemukan"
                }
        else:
            # Mengambil semua data dan mengubahnya menjadi list of dict
            data = [t.to_dict() for t in select(t for t in TransaksiPenerimaan)]
            resp.media = {"status": True, "data": data}

    @db_session
    def on_post(self, req, resp):
        """
        Menambah data transaksi penerimaan baru.
        Mencakup validasi tipe data nominal (int) dan tanggal (date).
        """
        data = req.media
        try:
            # Validasi & Konversi tipe data Tanggal (YYYY-MM-DD)
            try:
                tanggal_obj = datetime.strptime(data['tanggal'], "%Y-%m-%d").date()
            except (ValueError, KeyError):
                resp.status = falcon.HTTP_400
                resp.media = {"status": False, "message": "Format tanggal salah atau tidak ada (Gunakan YYYY-MM-DD)"}
                return

            # Validasi & Konversi tipe data Nominal ke Integer
            try:
                nominal_int = int(data['nominal'])
            except (ValueError, KeyError):
                resp.status = falcon.HTTP_400
                resp.media = {"status": False, "message": "Nominal harus berupa angka integer"}
                return

            # Menyimpan data baru sesuai dengan struktur form Frontend
            transaksi = TransaksiPenerimaan(
                jenis=data['jenis'],
                nominal=nominal_int,
                sumber=data['sumber'],
                menyetujui=data['menyetujui'],
                tanggal=tanggal_obj,
                keterangan=data.get('keterangan', '')
            )

            resp.status = falcon.HTTP_201
            resp.media = {
                "status": True,
                "message": "Data transaksi penerimaan berhasil disimpan",
                "data": transaksi.to_dict()
            }
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": False, "message": str(e)}

    @db_session
    def on_put(self, req, resp, id):
        """
        Mengupdate/Edit data transaksi penerimaan secara keseluruhan berdasarkan ID.
        """
        data = req.media
        try:
            transaksi = TransaksiPenerimaan[id]

            # Update data jika dikirimkan di payload, jika tidak gunakan data lama
            transaksi.jenis = data.get('jenis', transaksi.jenis)
            transaksi.sumber = data.get('sumber', transaksi.sumber)
            transaksi.menyetujui = data.get('menyetujui', transaksi.menyetujui)
            transaksi.keterangan = data.get('keterangan', transaksi.keterangan)

            # Validasi & Update Tanggal jika diubah
            if 'tanggal' in data:
                try:
                    transaksi.tanggal = datetime.strptime(data['tanggal'], "%Y-%m-%d").date()
                except ValueError:
                    resp.status = falcon.HTTP_400
                    resp.media = {"status": False, "message": "Format tanggal salah (Gunakan YYYY-MM-DD)"}
                    return

            # Validasi & Update Nominal jika diubah
            if 'nominal' in data:
                try:
                    transaksi.nominal = int(data['nominal'])
                except ValueError:
                    resp.status = falcon.HTTP_400
                    resp.media = {"status": False, "message": "Nominal harus berupa angka integer"}
                    return

            resp.media = {
                "status": True,
                "message": "Data transaksi penerimaan berhasil diupdate",
                "data": transaksi.to_dict()
            }
        except Exception:
            resp.status = falcon.HTTP_404
            resp.media = {
                "status": False,
                "message": "Data transaksi penerimaan tidak ditemukan"
            }

    @db_session
    def on_delete(self, req, resp, id):
        """
        Menghapus data transaksi penerimaan berdasarkan ID.
        """
        try:
            transaksi = TransaksiPenerimaan[id]
            transaksi.delete()
            resp.media = {
                "status": True,
                "message": "Data transaksi penerimaan berhasil dihapus"
            }
        except Exception:
            resp.status = falcon.HTTP_404
            resp.media = {
                "status": False,
                "message": "Data transaksi penerimaan tidak ditemukan"
            }
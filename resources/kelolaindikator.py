import falcon
from pony.orm import db_session, select
from models.schema import Surat, Indikator


# ==========================================
# RESOURCE UNTUK DATA SURAT (Tab: Surat)
# ==========================================
class SuratResource:
    @db_session
    def on_get(self, req, resp, id=None):
        if id:
            try:
                item = Surat[id]
                resp.media = {"status": True, "data": item.to_dict()}
            except Exception:
                resp.status = falcon.HTTP_404
                resp.media = {"status": False, "message": "Data surat tidak ditemukan"}
        else:
            # Mengambil semua data surat
            data = [item.to_dict() for item in select(s for s in Surat)]
            resp.media = {"status": True, "data": data}

    @db_session
    def on_post(self, req, resp):
        data = req.media
        try:
            # Validasi field wajib sesuai form input frontend
            item = Surat(
                noSurat=data.get('noSurat'),
                judul=data.get('judul'),
                tanggal=data.get('tanggal'),
                jenis=data.get('jenis'),
                deskripsi=data.get('deskripsi', '')
            )
            resp.status = falcon.HTTP_201
            resp.media = {"status": True, "message": "Data surat berhasil ditambahkan", "id": item.id}
        except Exception as e:
            resp.status = falcon.HTTP_400
            resp.media = {"status": False, "message": f"Gagal menambah surat: {str(e)}"}

    @db_session
    def on_put(self, req, resp, id):
        data = req.media
        try:
            item = Surat[id]
            item.set(**data)
            resp.media = {"status": True, "message": "Data surat berhasil diupdate"}
        except Exception as e:
            resp.status = falcon.HTTP_404
            resp.media = {"status": False, "message": "Data surat tidak ditemukan atau data tidak valid"}

    @db_session
    def on_delete(self, req, resp, id):
        try:
            item = Surat[id]
            item.delete()
            resp.media = {"status": True, "message": "Data surat berhasil dihapus"}
        except Exception:
            resp.status = falcon.HTTP_404
            resp.media = {"status": False, "message": "Data surat tidak ditemukan"}


# ==========================================
# RESOURCE UNTUK DATA INDIKATOR (Tab: Indikator)
# ==========================================
class IndikatorResource:
    @db_session
    def on_get(self, req, resp, id=None):
        if id:
            try:
                item = Indikator[id]
                resp.media = {"status": True, "data": item.to_dict()}
            except Exception:
                resp.status = falcon.HTTP_404
                resp.media = {"status": False, "message": "Indikator tidak ditemukan"}
        else:
            # Mengambil semua data indikator
            data = [item.to_dict() for item in select(i for i in Indikator)]
            resp.media = {"status": True, "data": data}

    @db_session
    def on_post(self, req, resp):
        data = req.media
        try:
            # Konversi bobot ke integer jika dikirim dalam bentuk string dari frontend
            bobot_val = int(data.get('bobot', 0)) if data.get('bobot') else 0

            item = Indikator(
                nama=data.get('nama'),
                tipe=data.get('tipe'),
                jenis=data.get('jenis'),
                bobot=bobot_val,
                urutan=int(data.get('urutan', 1)),
                relasi=data.get('relasi', 'Absen Masuk'),
                status=data.get('status', 'Aktif')
            )
            resp.status = falcon.HTTP_201
            resp.media = {"status": True, "message": "Indikator berhasil ditambahkan", "id": item.id}
        except Exception as e:
            resp.status = falcon.HTTP_400
            resp.media = {"status": False, "message": f"Gagal menambah indikator: {str(e)}"}

    @db_session
    def on_put(self, req, resp, id):
        data = req.media
        try:
            item = Indikator[id]

            # Jika bobot di-update, pastikan tipenya integer
            if 'bobot' in data:
                data['bobot'] = int(data['bobot'])
            if 'urutan' in data:
                data['urutan'] = int(data['urutan'])

            item.set(**data)
            resp.media = {"status": True, "message": "Indikator berhasil diupdate"}
        except Exception as e:
            resp.status = falcon.HTTP_404
            resp.media = {"status": False, "message": "Indikator tidak ditemukan atau data tidak valid"}

    @db_session
    def on_delete(self, req, resp, id):
        try:
            item = Indikator[id]
            item.delete()
            resp.media = {"status": True, "message": "Indikator berhasil dihapus"}
        except Exception:
            resp.status = falcon.HTTP_404
            resp.media = {"status": False, "message": "Indikator tidak ditemukan"}
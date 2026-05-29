import falcon
from pony.orm import db_session, select
# Mengimpor model JenisPenerimaan yang sudah disesuaikan dengan Frontend
from models.schema import JenisPenerimaan


class JenisPenerimaanResource:
    @db_session
    def on_get(self, req, resp, id=None):
        """
        Mengambil satu data berdasarkan ID atau mengambil seluruh daftar jenis penerimaan.
        """
        if id:
            try:
                # Mengambil data spesifik berdasarkan ID integer
                item = JenisPenerimaan[int(id)]
                resp.media = {"status": True, "data": item.to_dict()}
            except (ValueError, Exception):
                resp.status = falcon.HTTP_404
                resp.media = {
                    "status": False,
                    "message": "Data jenis penerimaan tidak ditemukan"
                }
        else:
            # Mengambil semua data dari database, diurutkan berdasarkan ID secara ascending
            data = [item.to_dict() for item in select(item for item in JenisPenerimaan).order_by(lambda item: item.id)]

            # Map struktur data agar nama key-nya serasi dengan konsumsi state di frontend (opsional namun aman)
            formatted_data = []
            for item in data:
                formatted_data.append({
                    "id": item['id'],
                    "kodeAkun": item['kode_akun_penerimaan'],  # Menyesuaikan {item.kodeAkun} di table frontend
                    "kode": item['kode_akun_penerimaan'],  # Menyesuaikan {item.kode} di table frontend
                    "nama": item['nama_akun_penerimaan'],  # Menyesuaikan {item.nama} di table frontend
                    "jenis": item['jenis'],  # Menyesuaikan {item.jenis} di table frontend
                    "keterangan": item['keterangan'],
                    "status": item['status'],  # Menyesuaikan {item.status} di table frontend
                    "akunHarta": item['akun_harta'],
                    "akunPendapatan": item['akun_pendapatan']
                })

            resp.media = {"status": True, "data": formatted_data}

    @db_session
    def on_post(self, req, resp):
        """
        Menambah data Jenis Penerimaan baru berdasarkan input Form Frontend.
        """
        data = req.media
        try:
            # Validasi input wajib dari Form Frontend
            required_fields = ['akun_harta', 'jenis', 'akun_pendapatan', 'kode_akun_penerimaan', 'nama_akun_penerimaan',
                               'status']
            for field in required_fields:
                if field not in data or str(data[field]).strip() == "" or data[field] == "Pilih Status":
                    resp.status = falcon.HTTP_400
                    resp.media = {"status": False,
                                  "message": f"Field '{field}' tidak boleh kosong dan harus dipilih dengan benar"}
                    return

            # Menyimpan data baru sesuai dengan struktur form komponen React
            new_jenis = JenisPenerimaan(
                akun_harta=data['akun_harta'],
                jenis=data['jenis'],
                akun_pendapatan=data['akun_pendapatan'],
                keterangan=data.get('keterangan', '-'),
                kode_akun_penerimaan=data['kode_akun_penerimaan'],
                nama_akun_penerimaan=data['nama_akun_penerimaan'],
                status=data['status']
            )

            # Memastikan data tersimpan untuk mendapatkan ID baru
            new_jenis.flush()

            resp.status = falcon.HTTP_201
            resp.media = {
                "status": True,
                "message": "Data jenis penerimaan berhasil disimpan",
                "data": new_jenis.to_dict()
            }
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": False, "message": str(e)}

    @db_session
    def on_put(self, req, resp, id):
        """
        Mengubah / Edit data konfigurasi Jenis Penerimaan secara keseluruhan berdasarkan ID.
        """
        data = req.media
        try:
            # Cari baris data berdasarkan ID target
            item = JenisPenerimaan[int(id)]

            # Lakukan update field jika dikirimkan oleh payload Frontend, jika tidak pakai nilai lama
            item.akun_harta = data.get('akun_harta', item.akun_harta)
            item.jenis = data.get('jenis', item.jenis)
            item.akun_pendapatan = data.get('akun_pendapatan', item.akun_pendapatan)
            item.keterangan = data.get('keterangan', item.keterangan)
            item.kode_akun_penerimaan = data.get('kode_akun_penerimaan', item.kode_akun_penerimaan)
            item.nama_akun_penerimaan = data.get('nama_akun_penerimaan', item.nama_akun_penerimaan)

            # Jaga agar status tidak terset ke default pilihan jika tidak sengaja terkirim teks placeholder
            if 'status' in data and data['status'] != "Pilih Status":
                item.status = data['status']

            resp.media = {
                "status": True,
                "message": "Data jenis penerimaan berhasil diperbarui",
                "data": item.to_dict()
            }
        except (ValueError, Exception):
            resp.status = falcon.HTTP_404
            resp.media = {
                "status": False,
                "message": "Data jenis penerimaan tidak ditemukan atau gagal diperbarui"
            }

    @db_session
    def on_delete(self, req, resp, id):
        """
        Menghapus data Jenis Penerimaan berdasarkan ID (Aksi tombol FaTrash).
        """
        try:
            item = JenisPenerimaan[int(id)]
            item.delete()

            resp.media = {
                "status": True,
                "message": "Data jenis penerimaan berhasil dihapus"
            }
        except (ValueError, Exception):
            resp.status = falcon.HTTP_404
            resp.media = {
                "status": False,
                "message": "Data jenis penerimaan tidak ditemukan"
            }
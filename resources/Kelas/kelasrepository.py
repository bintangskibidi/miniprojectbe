from pony.orm import db_session
from entitas.kelas.models import KelasDB


@db_session
def get_all_kelas_db():
    return [
        {
            "id": k.id,
            "kode": k.kode,
            "nama": k.nama
        }
        for k in KelasDB.select()
    ]


@db_session
def insert_kelas_db(data):
    k = KelasDB(
        kode=data.get("kode"),
        nama=data.get("nama")
    )

    return {
        "id": k.id,
        "kode": k.kode,
        "nama": k.nama
    }


@db_session
def update_kelas_db(id, data):
    k = KelasDB.get(id=id)

    if not k:
        return {"message": "Data tidak ditemukan"}

    k.kode = data.get("kode")
    k.nama = data.get("nama")

    return {
        "id": k.id,
        "kode": k.kode,
        "nama": k.nama
    }


@db_session
def delete_kelas_db(id):
    k = KelasDB.get(id=id)

    if not k:
        return {"message": "Data tidak ditemukan"}

    k.delete()

    return {"message": "Data berhasil dihapus"}
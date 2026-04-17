import json
from entitas.kelas import services


class KelasResource:

    def on_get(self, req, resp):
        resp.media = services.get_all_kelas_db()

    def on_post(self, req, resp):
        data = req.media
        resp.media = services.insert_kelas_db(data)


class KelasWithIdResource:

    def on_put(self, req, resp, id):
        data = req.media
        resp.media = services.update_kelas_db(int(id), data)

    def on_delete(self, req, resp, id):
        resp.media = services.delete_kelas_db(int(id))
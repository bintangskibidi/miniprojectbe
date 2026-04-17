from entitas.kelas.resources import KelasResource, KelasWithIdResource


def kelas_routes(api):

    api.add_route("/api/kelas", KelasResource())

    api.add_route("/api/kelas/{id:int}", KelasWithIdResource())
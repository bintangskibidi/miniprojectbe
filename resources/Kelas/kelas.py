from pony.orm import PrimaryKey, Optional
from util.db_util import db2

class KelasDB(db2.Entity):
    _table_ = "kelas"

    id = PrimaryKey(int, auto=True)
    kode = Optional(str)
    nama = Optional(str)
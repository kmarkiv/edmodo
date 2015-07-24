__author__ = 'vikram'

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session


class Db:
    def __init__(self, engine):
        self.data = []
        self.base = automap_base()
        self.base.prepare(engine, reflect=True)
        self.db = Session(engine)

    def get_data(self, sql):
        a = self.db.execute(sql)
        data = [dict(r) for r in a]
        return data

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
        try:
            # converting result proxy to a dictionary
            results = self.db.execute(sql)
            return self.get_dict_data(results)
        except Exception as e:
            return []

    def get_dict_data(self, results):
        data = [dict(r) for r in results]
        return data

    def sanitize_int(self, data):
        try:
            return int(data)
        except Exception as e:
            return 0

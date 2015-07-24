from sqlalchemy import text

from db import Db

__author__ = 'vikram'


class Apps(Db):
    def get_recent(self, start=0, count=30):
        sql = "SELECT * FROM  spotlight_apps LIMIT %s,%s" % (start, count)
        return self.get_data(sql)

    def get_user(self, user_id, start=0, count=50):
        sql = "SELECT * FROM  spotlight_apps WHERE owner_id=%s LIMIT %s,%s" % (self.sanitize_int(user_id), start, count)
        return self.get_data(sql)

    def search_app(self, term, start=0, count=50):
        sql = text("""SELECT * FROM  spotlight_apps WHERE MATCH (title,long_desc) AGAINST (:term) LIMIT %s,%s""" % (
            start, count))
        conn = self.db.connection()
        results = conn.execute(sql, term=term).fetchall()
        return self.get_dict_data(results)

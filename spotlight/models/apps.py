from db import Db

__author__ = 'vikram'


class Apps(Db):
    def get_recent(self, start=0, count=30):
        sql = "SELECT * FROM  spotlight_apps LIMIT %s,%s" % (start, count)
        return self.get_data(sql)

    def get_user(self, user_id, start=0, count=50):
        sql = "SELECT * FROM  spotlight_apps WHERE owner_id=%s LIMIT %s,%s" % (user_id, start, count)
        return self.get_data(sql)

    def search_app(self, term, start=0, count=50):
        sql = "SELECT * FROM  spotlight_apps WHERE MATCH (title,long_desc) AGAINST ('%s') LIMIT %s,%s" % (
            term, start, count)
        return self.get_data(sql)

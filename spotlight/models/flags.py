__author__ = 'vikram'

from db import Db


class Flags(Db):
    def add_data(self, app_id, flags):
        essay_drafts = self.base.classes.spotlight_apps_flags
        for flag in flags:
            c = essay_drafts(app_id=app_id, flag_id=flag)
            self.db.add(c)
        self.db.commit()
        return True

    def get_list(self):
        sql = "SELECT a.*,f.flag,af.id as fid FROM spotlight_apps_flags af,spotlight_apps a,spotlight_flags f " \
              "WHERE a.id=af.app_id AND af.flag_id=f.id"
        return self.get_data(sql)

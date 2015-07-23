__author__ = 'vikram'
import requests
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

import config

TERMS = ["math", "mitosis", "fractions"]
SPOTLIGHT_URL = "https://spotlight.edmodo.com/api/search/"


class Scraper:
    def __init__(self, engine):
        self.data = []
        self.base = automap_base()
        self.base.prepare(engine, reflect=True)
        self.db = Session(engine)

    def scrape(self, term, count=100):
        api_data = self.fetch_api(term, count)
        for app in api_data:
            self.add_record(app)

    def fetch_api(self, term, count):
        url = SPOTLIGHT_URL
        params = dict(q=term, page_length=count)
        data = requests.get(url=url, params=params)
        return data.json()['hits']

    def add_record(self, data):
        data = data['_source']
        apps = self.base.classes.spotlight_apps
        grades = self.base.classes.spotlight_apps_grades
        subjects = self.base.classes.spotlight_apps_subjects
        resource_types = self.base.classes.spotlight_apps_resource_types
        app = apps(creation_date=data['creation_date'], currency=data['currency'], title=data['title'],
                   owner_id=data['owner_id'], owner_name=data['owner']['first_name'], price=data['price'],
                   url=data['url'], img_path=data['img_path'], seller_thumb_url=data['seller_thumb_url'],
                   long_desc=data['long_desc'], avg_rating=data['avg_rating'], id=data['id'],
                   num_raters=data['num_raters'])
        self.db.add(app)
        for grade_text in data['grades']:
            grade = grades(app_id=data['id'], grade=grade_text)
            self.db.add(grade)

        for subject_text in data['subjects']:
            grade = subjects(app_id=data['id'], subject=subject_text)
            self.db.add(grade)

        for resource in data['resource_types']:
            grade = resource_types(app_id=data['id'], resource=resource)
            self.db.add(grade)

        self.db.commit()

    def clear_data(self):
        sql = "TRUNCATE TABLE `spotlight_apps_subjects`"
        self.db.execute(sql)
        sql = "TRUNCATE TABLE `spotlight_apps_resource_types`"
        self.db.execute(sql)
        sql = "TRUNCATE TABLE `spotlight_apps_grades`"
        self.db.execute(sql)
        sql = "TRUNCATE TABLE `spotlight_apps`"
        self.db.execute(sql)
        self.db.commit()


def main():
    engine = create_engine(config.DB_URL, convert_unicode=True, encoding="utf-8")
    sp = Scraper(engine)
    sp.clear_data()
    for term in TERMS:
        sp.scrape(term)


if __name__ == "__main__":
    main()

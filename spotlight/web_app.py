__author__ = 'vikram'
from flask import render_template, Flask, request
from sqlalchemy import create_engine

from models.apps import Apps
from models.flags import Flags

import config
from api_response import api_response

app = Flask(__name__)
engine = create_engine(config.DB_URL, convert_unicode=True, encoding="utf-8")


@app.route('/')
def home():
    return render_template('layout.html', title="Spotlight")


@app.route('/api/apps')
def search():
    apps = Apps(engine)
    return api_response({"apps": apps.get_recent()})


@app.route('/api/apps/users/<user_id>')
def search_user(user_id):
    apps = Apps(engine)
    return api_response({"apps": apps.get_user(user_id)})


@app.route('/api/apps/search')
def apps_search():
    apps = Apps(engine)
    term = request.args.get("term", None)
    return api_response({"apps": apps.search_app(term)})


@app.route('/api/flags', methods=["POST"])
def post_flag():
    flags = Flags(engine)
    flag_ids = request.form.getlist("flags[]", None)
    app_id = request.form.get("app_id", 0)
    return api_response({"apps": flags.add_data(app_id, flag_ids)})


@app.route('/api/flags')
def get_flags():
    flags = Flags(engine)
    return api_response({"flags": flags.get_list()})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

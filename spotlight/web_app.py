__author__ = 'vikram'

from flask import render_template, Flask
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

import config

app = Flask(__name__)
engine = create_engine(config.DB_URL, convert_unicode=True, encoding="utf-8")
Base = automap_base()
Base.prepare(engine, reflect=True)
db = Session(engine)

@app.route('/')
def home():
    return render_template('views/home.html', title="Login")


@app.route('/api/search')
def search():
    return render_template('views/home.html', title="Login")


@app.route('/api/apps/<app_id>/flag', methods=["POST"])
def flag(app_id):
    return render_template('views/home.html', title="Login")


@app.route('/api/flags')
def flags():
    return render_template('views/home.html', title="Login")


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

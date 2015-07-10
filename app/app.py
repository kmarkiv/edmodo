__author__ = 'vikram'

from functools import wraps
from cStringIO import StringIO
from optparse import OptionParser
import os

from flask import Flask, render_template, request, redirect, send_from_directory, url_for, g, session, flash
from flask_login import login_user, logout_user, current_user, UserMixin
from iniparse import INIConfig
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from flask.ext.login import LoginManager, login_required

# User not found exception
class UserNotFoundError(Exception):
    pass


# User object from database
class SqlUser(UserMixin):
    def __init__(self, data):
        # if not data
        if data is None:
            raise UserNotFoundError()

        try:
            self.id = data.id
            self.data = data
            self.role = data.role
        except Exception as e:
            print e


TEACHER = "teacher"
STUDENT = "student"
UWSGI_ENV = 'SERVER_ENV'
PRODUCTION_ENV = 'production'

# for local environment
# python app.py -e kmarkiv
parser = OptionParser(usage="Usage: %prog [options] filename")
parser.add_option("-e", "--environment", dest="environment", help="Set the application environment")
(options, args) = parser.parse_args()
if options.environment:
    ENV = options.environment
else:
    ENV = os.environ.get(UWSGI_ENV, PRODUCTION_ENV)

# store config in text to save read write
config_text = """
[production]
database = edmodo_interview
username = root
password = worldpeace2
debug = enabled
host =127.0.0.1
url = edmodo.kmarkiv.com

[kmarkiv]
database = edmodo_interview
username = root
password = worldpeace
debug = enabled
host =127.0.0.1
url = http://127.0.0.1:5000

[dev]
database = edmodo_interview
username = root
password =
debug = enabled
host =127.0.0.1
url = http://127.0.0.1:5000

"""


def get_data(env="production"):
    f = StringIO(config_text)
    cfg = INIConfig(f)
    config = cfg[env]
    return config


app = Flask(__name__)
app.config['SECRET_KEY'] = '123456790'
app.config['DATA'] = get_data(ENV)
app.config['SQLAlchemy_DATABASE_URI'] = "mysql://%s:%s@%s/%s" % (
    app.config['DATA']['username'], app.config['DATA']['password'], app.config['DATA']['host'],
    app.config['DATA']['database'])
engine = create_engine(app.config['SQLAlchemy_DATABASE_URI'])

Base = automap_base()
Base.prepare(engine, reflect=True)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
db = Session(engine)


# get user from database
@login_manager.user_loader
def load_user(id):
    return get_user_by_id(id)


def get_user_by_id(user_id):
    Users = Base.classes.users
    user = db.query(Users).filter_by(id=user_id).first()
    return SqlUser(user) if user else None


# wrapper for teacher access
def teacher_login(f):
    @login_required
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.data.role != TEACHER:
            # flash("You are not a teacher")
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)

    return decorated_function


# login page
@app.route('/')
def home():
    role = request.args.get("role", "teacher")
    password = "demo"
    if role == "teacher":
        user = "teacher@demo.com"
    else:
        user = "student1@demo.com"
    return render_template('views/login.html', user=user, password=password,title="Login")


# login page
@app.route('/login')
def login():
    return home()


# redirect based on the role
@app.route("/dashboard")
@login_required
def dashboard():
    if current_user.role == TEACHER:
        return redirect("/teachers")
    else:
        return redirect("/students")


# check login and then use
@app.route('/login/check', methods=["POST"])
def login_check():
    session['next'] = request.args.get('next', "/dashboard")
    if request.method == 'POST':
        email = request.form.get('email', "")
        password = request.form.get('password', "")
        Users = Base.classes.users
        u1 = db.query(Users).filter_by(email=email).first()

        if u1:
            if password == u1.password:
                user = SqlUser(u1)
                g.user = current_user
                login_user(user, remember=True)
                if "next" in session:
                    return redirect(session['next'])
                else:
                    return dashboard()
    return render_template('views/login.html')


# List of all homeworks
@app.route('/teachers')
@teacher_login
def teachers():
    essay = db.execute(
        "SELECT *,CASE WHEN CURDATE() > due_date THEN 1 ELSE 0 END as past_due FROM homeworks WHERE "
        "teacher_id=%s" % current_user.data.id)
    return render_template('views/teachers/home.html', essays=essay,title="Homeworks")


# Home work
@app.route('/teachers/homework/<homework_id>')
@teacher_login
def teachers_homework(homework_id):
    sql = "SELECT *,CASE WHEN CURDATE() > due_date THEN 1 ELSE 0 END as past_due FROM homeworks WHERE id='%s'" % (
        homework_id)
    homework = db.execute(sql).first()
    # The teacher needs see who has not submitted and the number of submissions
    # Left join submissions with students
    # Count of submissions gives the total submissions when grouped by student_id
    sql = "SELECT * , COUNT( submission ) AS submits FROM (SELECT hs.id,s.homework_id,h.due_date,h. title,h.question," \
          "hs.updated_at as updated_at,u.name, u.email, s.student_id, hs.submission FROM users u, homeworks h, " \
          "homework_students s LEFT JOIN homework_submissions hs ON s.student_id = hs.student_id AND hs.homework_id=%s " \
          "WHERE s.homework_id = h.id AND h.id =%s AND u.id = s.student_id ORDER BY hs.id DESC) tmp GROUP BY " \
          "student_id" % (
              homework_id, homework_id)
    essay = db.execute(sql
                       )
    return render_template('views/teachers/homeworks.html', essays=essay, homework=homework,title=homework.title)


@app.route('/teachers/homework/<homework_id>/student/<student_id>')
@teacher_login
def teachers_homework_student(homework_id, student_id):
    # Check if assignment is past due and have an option to submit
    sql = "SELECT *,CASE WHEN CURDATE() > due_date THEN 1 ELSE 0 END as past_due FROM homeworks WHERE id='%s'" % (
        homework_id)
    homework = db.execute(sql).first()
    sql = "SELECT * FROM users WHERE id='%s'" % (student_id)
    users = db.execute(sql).first()
    sql = "SELECT h.*,u.name,u.email FROM homework_submissions h,users u WHERE h.homework_id=%s " \
          "AND u.id=h.student_id AND student_id=%s ORDER BY h.id DESC" % (
              homework_id, student_id)
    essay = db.execute(sql
                       )
    return render_template('views/teachers/submissions.html', essays=essay, homework=homework, users=users,title=users.name)


@app.route('/students')
@login_required
def students():

    # List of homework assigned and submissions
    sql = "SELECT s.updated_at as updated,CASE WHEN CURDATE() > h.due_date THEN 1 ELSE 0 END as past_due,h.*," \
          "COUNT(submission) as submits FROM homework_students s,homeworks h LEFT JOIN homework_submissions hs " \
          "ON hs.homework_id=h.id WHERE s.homework_id=h.id AND h.id AND s.student_id=%s GROUP BY s.homework_id" % (
              current_user.data.id)
    essay = db.execute(sql
                       )
    return render_template('views/students/home.html', essays=essay,title="My Homework")


@app.route('/students/homework/<homework_id>')
@login_required
def students_homework(homework_id):
    sql = "SELECT *,CASE WHEN CURDATE() > due_date THEN 1 ELSE 0 END as past_due FROM homeworks WHERE id='%s'" % (
        homework_id)
    homework = db.execute(sql).first()
    # List of submissions
    sql = "SELECT h.*,u.name,u.email FROM homework_submissions h,users u WHERE h.homework_id=%s AND " \
          "u.id=h.student_id AND student_id=%s ORDER BY h.id DESC" % (
              homework_id, current_user.data.id)
    essay = db.execute(sql)

    return render_template('views/students/submissions.html', essays=essay, homework=homework,title=homework.title)


@app.route('/students/homework/<homework_id>/post', methods=["POST"])
@login_required
def students_homework_post(homework_id):
    # submit homework if due date has not passed
    sql = "SELECT *,CASE WHEN CURDATE() > due_date THEN 1 ELSE 0 END as past_due FROM homeworks WHERE id='%s'" % (
        homework_id)
    homework = db.execute(sql).first()
    if not homework.past_due:
        essay_id = request.form.get('submission', "")
        essay_drafts = Base.classes.homework_submissions
        c = essay_drafts(submission=essay_id, seen=0, created_at="", homework_id=homework_id,
                         student_id=current_user.data.id)
        db.add(c)
        db.commit()
        flash("You have submitted your assignment")

    return redirect("/students/homework/%s" % homework_id)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.errorhandler(500)
def not_found(error):
    db.rollback()
    return render_template('home.html'), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

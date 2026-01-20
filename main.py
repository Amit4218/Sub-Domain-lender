from flask import Flask, redirect, render_template, request, session, url_for

from app.auth import login_user, register_user
from app.core import create_record, delete_record
from app.middleware import isLoggedIn
from config import db
from utils import DATABASE_URL, SECRET_KEY
from utils.get_user_records import get_user_records

app = Flask(__name__)


app.secret_key = SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app=app)
with app.app_context():
    db.create_all()


@app.route("/health", methods=["GET"])
def root():
    return {"status": "ok"}, 200


@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")


@app.route("/about", methods=["GET"])
def about():
    return render_template("about.html")


@app.errorhandler(Exception)
def error(e):
    return render_template("error.html", error=e)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email: str = request.form.get("email")
    password: str = request.form.get("password")

    result, error = login_user(email, password)

    if error:
        return render_template("login.html", error=error)

    session["user_id"] = result["id"]
    session["email"] = result["email"]

    return redirect(url_for("dashboard"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    email: str = request.form.get("email")
    password: str = request.form.get("password")

    result, error = register_user(email, password)

    if error:
        return render_template("register.html", error=error)

    session["user_id"] = result["id"]
    session["email"] = result["email"]

    return redirect("dashboard")


@app.route("/logout", methods=["POST"])
def logout():
    user_id = session.get("user_id")
    email = session.get("email")

    if not user_id or not email:
        return render_template("login.html", error="Error Logging Out!")
    else:
        session.clear()

    return redirect(url_for("login"))


@app.route("/dashboard", methods=["GET"])
@isLoggedIn
def dashboard():
    user_id = session.get("user_id")
    data = get_user_records(user_id=user_id)
    return render_template("dashboard.html", records=data)


@app.route("/add-record", methods=["POST"])
@isLoggedIn
def create_dns_record():
    user_id = session.get("user_id")

    if not user_id:
        return render_template("login.html", error="User must be logged in first..")

    type = request.form.get("type")
    name = request.form.get("name")
    content = request.form.get("content")
    ttl = request.form.get("ttl")

    if not type or not name or not content:
        return render_template(
            "dashboard.html", error="Name, Content and Type is required!"
        )

    error = create_record(id=user_id, name=name, type=type, content=content, ttl=ttl)

    if error:
        records = get_user_records(user_id=user_id)
        return render_template("dashboard.html", error=error, records=records)

    return redirect(url_for("dashboard"))


@app.route("/delete-record/<record_id>", methods=["POST"])
@isLoggedIn
def delete_dns_record(record_id):
    user_id = session.get("user_id")

    if not user_id:
        return render_template("login.html", error="User must be logged in first..")

    error = delete_record(user_id=user_id, record_id=record_id)

    if error:
        records = get_user_records(user_id=user_id)
        return render_template("dashboard.html", error=error, records=records)

    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    app.run(debug=True)

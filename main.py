from flask import Flask, redirect, render_template, request, session, url_for

from app.auth import login_user, register_user
from config import db
from utils import DATABASE_URL, SECRET_KEY

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


if __name__ == "__main__":
    app.run(debug=True)

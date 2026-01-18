from flask import Flask, render_template, request, session, url_for

from app.auth import login_user, register_user
from config import db

app = Flask("__name__")


app.secret_key = "random_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///local.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app=app)
with app.app_context():
    db.create_all()


@app.route("/health")
def root():
    return render_template("home.html")


@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    try:
        if request.method == "GET":
            return render_template(url_for("login"))

        email: str = request.form["email"]
        password: str = request.form["password"]

        result = login_user(email, password)

        if result:
            session["user_id"] = result["id"]
            session["email"] = result["email"]

        return render_template(url_for("dashboard"))
    except ValueError as e:
        return render_template(url_for("login"), error=e)
    except Exception:
        return


@app.route("/register", methods=["GET", "POST"])
def register():
    try:
        if request.method == "GET":
            return render_template(url_for("register"))

        email: str = request.form["email"]
        password: str = request.form["password"]

        result = register_user(email, password)

        if result:
            session["user_id"] = result["id"]
            session["email"] = result["email"]

        return render_template(url_for("dashboard"))

    except ValueError as e:
        return render_template(url_for("register"), error=e)
    except Exception:
        return


@app.route("/logout", methods=["POST"])
def logout():
    user_id = session.get("user_id")
    email = session.get("email")

    if not user_id or email:
        return render_template(url_for("login"), error="Error Logging Out!")
    else:
        session.clear()

    return render_template(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)

from app.models import User
from config import db


def login_user(email: str, password: str) -> dict:
    if not email or password:
        raise ValueError("Both Feilds Must Be Filled")

    user = db.session.query(User).filter_by(email=email).first()

    if not user:
        raise ValueError("Invalid Credientials")

    if not user.check_password(password=password):
        raise ValueError("Invalid Credientials")

    data = {"id": user.id, "email": user.email}

    return data


def register_user(email: str, password: str) -> dict:
    if not email or password:
        raise ValueError("Both Feilds Must Be Filled")

    user = db.session.query(User).filter_by(email=email).first()

    if user is not None:
        raise Exception("User Already Exists!")

    new_user = User(email=email)
    new_user.hash_password(password=password)

    db.session.add(new_user)
    db.session.commit()
    db.session.refresh(new_user)

    data = {"id": new_user.id, "email": new_user.email}

    return data

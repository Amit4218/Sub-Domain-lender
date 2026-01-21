import uuid

from sqlalchemy import select

from app.models import User
from config import db
from utils import BASE_URL
from utils.email_sender import send_email


def login_user(email: str, password: str):
    if not email or not password:
        return None, "Both Fields Must Be Filled"

    user = db.session.query(User).filter_by(email=email).first()

    if not user:
        return None, "Invalid Credientials"

    if not user.check_password(password=password):
        return None, "Invalid Credientials"

    data = {"id": user.id, "email": user.email}

    return data, None


def register_user(email: str, password: str):
    if not email or not password:
        return None, "Both Fields Must Be Filled"

    user = db.session.query(User).filter_by(email=email).first()

    if user is not None:
        return None, "User Already Exists!"

    new_user = User(email=email)
    new_user.hash_password(password=password)

    data = {"id": new_user.id, "email": new_user.email}

    user_token = uuid.uuid3(uuid.NAMESPACE_DNS, new_user.email)

    final_url = f"{BASE_URL}?token={user_token}&email={email}"

    sended_email = send_email(
        user_email=new_user.email,
        user_name=new_user.email.split("@")[0],
        token=final_url,
    )

    if not sended_email["id"]:
        return None, "Error registering, please try again.."

    db.session.add(new_user)
    db.session.commit()
    db.session.refresh(new_user)

    return data, None


def verify_user_token(token, email):
    is_token_valid = uuid.uuid3(uuid.NAMESPACE_DNS, email)

    if not is_token_valid:
        return None, "Invalid token! please register again."

    user = db.session.execute(
        select(User).where(User.email == email)
    ).scalar_one_or_none()

    if not user:
        return None, "User not found! please register again."

    user.is_email_verified = True

    db.session.commit()
    db.session.refresh(user)

    data = {"id": user.id, "email": user.email}

    return data, None

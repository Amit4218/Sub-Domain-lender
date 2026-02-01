import uuid

from sqlalchemy import select

from app.models import User
from config import db
from utils import BASE_URL
from utils.email_sender import send_email, send_reset_password_email


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

    final_url = f"{BASE_URL}/verify?token={user_token}&email={email}"

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

    if str(token) != str(is_token_valid):
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


def verify_user_and_send_email(email):
    if not email:
        return None, "Email is required!"

    user = db.session.execute(
        select(User).where(User.email == email)
    ).scalar_one_or_none()

    if not user:
        return None, "User not found! please check your email!"

    user_token = uuid.uuid3(uuid.NAMESPACE_DNS, str(user.id))

    final_url = f"{BASE_URL}/reset_password?token={user_token}&id={user.id}"

    sended_email = send_reset_password_email(
        user_email=email, user_name=email.split("@")[0], token=final_url
    )

    if not sended_email["id"]:
        return None, "Error sending Email, please try again.."

    return True, None


def verify_user_and_update_password(token, user_id, new_password):
    if not token or not user_id:
        return None, "Something went wrong! please try again!"

    if not new_password:
        return None, "No password provoded!"

    verify_token = str(uuid.uuid3(uuid.NAMESPACE_DNS, user_id))

    if token != verify_token:
        return None, "Something went wrong! please try again!"

    user = db.session.execute(
        select(User).where(User.id == uuid.UUID(user_id))
    ).scalar_one_or_none()

    if not user:
        return None, "Something went wrong! please try again!"

    user.hash_password(new_password)

    db.session.commit()

    return True, None

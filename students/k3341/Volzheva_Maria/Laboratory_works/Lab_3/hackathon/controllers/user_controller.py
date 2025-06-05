from fastapi import Depends, HTTPException
from sqlmodel import select, Session
from typing import List
from hackathon.models import User, UserAuth, UserUpdate, UserPublic, UserProfile, UserRole
from hackathon.auth import auth_handler
import os


def login_user(user: UserAuth, session: Session) -> dict:
    user_found = session.exec(select(User).where(User.username == user.username)).first()
    if user_found is None:
        raise HTTPException(status_code=400, detail='Invalid username')
    if not auth_handler.verify_password(user.password, user_found.password):
        raise HTTPException(status_code=401, detail='Invalid password')
    token = auth_handler.encode_token(user_found.id)
    return {'token': token}


def register_user(user: UserAuth, session: Session) -> dict:
    existing_user = session.exec(select(User).where(User.username == user.username)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail='Username is taken')
    user.password = auth_handler.get_password_hash(user.password)
    user = User.model_validate(user)
    session.add(user)
    session.commit()
    session.refresh(user)
    token = auth_handler.encode_token(user.id)
    return {'token': token}


def set_admin_role(user_id: int, secret_code: str, session: Session) -> dict:
    if secret_code != os.getenv('LAB1_ADMIN_KEY'):
        raise HTTPException(status_code=403, detail='Code is not available')
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail='User not found')
    db_user.role = UserRole.admin
    session.add(db_user)
    session.commit()
    return {"ok": True}


def get_user_profile(user_id: int, session: Session) -> UserProfile:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user


def get_all_users(session: Session) -> List[UserPublic]:
    return session.exec(select(User)).all()


def get_user_by_id(user_id: int, session: Session) -> UserProfile:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user


def delete_user(user_id: int, session: Session) -> dict:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    session.delete(user)
    session.commit()
    return {"ok": True}


def update_user(user_id: int, updates: UserUpdate, session: Session) -> UserPublic:
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail='User not found')
    user_data = updates.model_dump(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

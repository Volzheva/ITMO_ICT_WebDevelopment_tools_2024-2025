from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import List
from hackathon.db import get_session
from hackathon.auth import auth_handler
from hackathon.models import UserAuth, UserUpdate, UserPublic, UserProfile
from hackathon.controllers import user_controller

router = APIRouter()


@router.post("/login")
def login(user: UserAuth, session: Session = Depends(get_session)) -> dict:
    return user_controller.login_user(user, session)


@router.post("/registration")
def register(user: UserAuth, session: Session = Depends(get_session)) -> dict:
    return user_controller.register_user(user, session)


@router.post("/set-admin/{user_id}")
def set_admin(user_id: int, secretCode: str, session: Session = Depends(get_session)):
    return user_controller.set_admin_role(user_id, secretCode, session)


@router.post("/get-profile")
def profile(authUserId=Depends(auth_handler.get_user), session: Session = Depends(get_session)) -> UserProfile:
    return user_controller.get_user_profile(authUserId, session)


@router.get("/get-all")
def get_all(session: Session = Depends(get_session)) -> List[UserPublic]:
    return user_controller.get_all_users(session)


@router.get("/get-one/{user_id}")
def get_one(user_id: int, session: Session = Depends(get_session)) -> UserProfile:
    return user_controller.get_user_by_id(user_id, session)


@router.delete("/delete-profile")
def delete(authUserId=Depends(auth_handler.get_user), session: Session = Depends(get_session)):
    return user_controller.delete_user(authUserId, session)


@router.patch("/update-profile")
def update(updates: UserUpdate, authUserId=Depends(auth_handler.get_user), session: Session = Depends(get_session)) -> UserPublic:
    return user_controller.update_user(authUserId, updates, session)

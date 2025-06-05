from fastapi import Depends, HTTPException
from sqlmodel import select
from typing import List

from hackathon.db import get_session
from hackathon.models import Hackathon, HackathonCreate, HackathonUpdate, HackathonFull, User, UserRole
from hackathon.auth import auth_handler


def get_all_hackathons(session=Depends(get_session)) -> List[Hackathon]:
    return session.exec(select(Hackathon)).all()


def get_hackathon_by_id(hackathon_id: int, session=Depends(get_session)) -> HackathonFull:
    return session.get(Hackathon, hackathon_id)


def create_hackathon(
    hackathon: HackathonCreate,
    authUserId=Depends(auth_handler.get_user),
    session=Depends(get_session)
) -> HackathonFull:
    auth_user = session.get(User, authUserId)
    if not auth_user or auth_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="User not available")
    hackathon = Hackathon.model_validate(hackathon)
    session.add(hackathon)
    session.commit()
    session.refresh(hackathon)
    return hackathon


def update_hackathon(
    hackathon_id: int,
    updates: HackathonUpdate,
    authUserId=Depends(auth_handler.get_user),
    session=Depends(get_session)
) -> HackathonFull:
    auth_user = session.get(User, authUserId)
    if not auth_user or auth_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="User not available")
    hackathon = session.get(Hackathon, hackathon_id)
    if not hackathon:
        raise HTTPException(status_code=404, detail="Hackathon not found")
    hackathon_data = updates.model_dump(exclude_unset=True)
    for key, value in hackathon_data.items():
        setattr(hackathon, key, value)
    session.add(hackathon)
    session.commit()
    session.refresh(hackathon)
    return hackathon


def delete_hackathon(
    hackathon_id: int,
    authUserId=Depends(auth_handler.get_user),
    session=Depends(get_session)
):
    auth_user = session.get(User, authUserId)
    if not auth_user or auth_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="User not available")
    hackathon = session.get(Hackathon, hackathon_id)
    if not hackathon:
        raise HTTPException(status_code=404, detail="Hackathon not found")
    session.delete(hackathon)
    session.commit()
    return {"ok": True}


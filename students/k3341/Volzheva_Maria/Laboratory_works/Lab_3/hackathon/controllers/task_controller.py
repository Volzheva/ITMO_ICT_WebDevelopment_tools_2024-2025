from fastapi import Depends, HTTPException
from sqlmodel import select
from typing import List

from hackathon.db import get_session
from hackathon.auth import auth_handler
from hackathon.models import Task, TaskFull, TaskCreate, TaskUpdate, User, UserRole


def get_all_tasks(session=Depends(get_session)) -> List[Task]:
    return session.exec(select(Task)).all()


def get_task_by_id(task_id: int, session=Depends(get_session)) -> TaskFull:
    return session.get(Task, task_id)


def create_task(
        task_data: TaskCreate,
        authUserId=Depends(auth_handler.get_user),
        session=Depends(get_session)
) -> TaskFull:
    auth_user = session.get(User, authUserId)
    if not auth_user or auth_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="User not available")

    task_model = Task.model_validate(task_data)
    session.add(task_model)
    session.commit()
    session.refresh(task_model)
    return task_model


def update_task(
        task_id: int,
        updates: TaskUpdate,
        authUserId=Depends(auth_handler.get_user),
        session=Depends(get_session)
) -> TaskFull:
    auth_user = session.get(User, authUserId)
    if not auth_user or auth_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="User not available")

    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task_data = updates.model_dump(exclude_unset=True)
    for key, value in task_data.items():
        setattr(task, key, value)

    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def delete_task(
        task_id: int,
        authUserId=Depends(auth_handler.get_user),
        session=Depends(get_session)
):
    auth_user = session.get(User, authUserId)
    if not auth_user or auth_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="User not available")

    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    session.delete(task)
    session.commit()
    return {"ok": True}

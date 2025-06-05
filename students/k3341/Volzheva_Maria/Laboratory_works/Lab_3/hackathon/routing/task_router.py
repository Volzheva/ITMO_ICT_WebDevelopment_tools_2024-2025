from fastapi import APIRouter
from typing import List

from hackathon.models import Task, TaskFull, TaskCreate, TaskUpdate
from hackathon.controllers import task_controller

router = APIRouter()


@router.get("/get-all", response_model=List[Task])
def tasks_list():
    return task_controller.get_all_tasks()


@router.get("/get-one/{task_id}", response_model=TaskFull)
def task_get_one(task_id: int):
    return task_controller.get_task_by_id(task_id)


@router.post("/create", response_model=TaskFull)
def create_task(task_data: TaskCreate):
    return task_controller.create_task(task_data)


@router.patch("/update/{task_id}", response_model=TaskFull)
def update_task(task_id: int, updates: TaskUpdate):
    return task_controller.update_task(task_id, updates)


@router.delete("/delete-task/{task_id}")
def delete_task(task_id: int):
    return task_controller.delete_task(task_id)

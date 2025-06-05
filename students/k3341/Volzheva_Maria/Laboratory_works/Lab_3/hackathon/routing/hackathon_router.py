from fastapi import APIRouter, Depends
from typing import List

from hackathon.models import Hackathon, HackathonFull, HackathonCreate, HackathonUpdate
from hackathon.controllers import hackathon_controller

router = APIRouter()


@router.get("/get-all", response_model=List[Hackathon])
def hackathons_list():
    return hackathon_controller.get_all_hackathons()


@router.get("/get-one/{hackathon_id}", response_model=HackathonFull)
def hackathon_get_one(hackathon_id: int):
    return hackathon_controller.get_hackathon_by_id(hackathon_id)


@router.post("/create", response_model=HackathonFull)
def hackathon_create(hackathon: HackathonCreate):
    return hackathon_controller.create_hackathon(hackathon)


@router.patch("/update/{hackathon_id}", response_model=HackathonFull)
def hackathon_update(hackathon_id: int, updates: HackathonUpdate):
    return hackathon_controller.update_hackathon(hackathon_id, updates)


@router.delete("/delete-hackathon/{hackathon_id}")
def hackathon_delete(hackathon_id: int):
    return hackathon_controller.delete_hackathon(hackathon_id)

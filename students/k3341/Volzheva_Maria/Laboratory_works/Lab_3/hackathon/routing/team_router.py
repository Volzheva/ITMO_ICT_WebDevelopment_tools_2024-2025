from fastapi import APIRouter, Depends
from typing import List
from hackathon.models import Team, TeamFull, TeamCreate, TeamUpdate
from hackathon.controllers import team_controller

router = APIRouter(prefix="/teams", tags=["Teams"])

@router.get("/get-all", response_model=List[Team])
def teams_list():
    return team_controller.get_all_teams()


@router.get("/get-one/{team_id}", response_model=TeamFull)
def team_get_one(team_id: int):
    return team_controller.get_one_team(team_id)


@router.post("/create", response_model=TeamFull)
def team_create(team: TeamCreate):
    return team_controller.create_team(team)


@router.post("/add-member/{team_id}/{user_id}", response_model=TeamFull)
def add_team_member(team_id: int, user_id: int, user_role: str | None = None):
    return team_controller.add_member(team_id, user_id, user_role)


@router.delete("/delete-member/{team_id}/{user_id}", response_model=TeamFull)
def delete_team_member(team_id: int, user_id: int):
    return team_controller.remove_member(team_id, user_id)


@router.patch("/update/{team_id}", response_model=TeamFull)
def team_update(team_id: int, updates: TeamUpdate):
    return team_controller.update_team(team_id, updates)


@router.delete("/delete-team/{team_id}")
def team_delete(team_id: int):
    return team_controller.delete_team(team_id)

from fastapi import APIRouter
from typing import List

from hackathon.models import Submission, SubmissionFull, SubmissionCreate
from hackathon.controllers import submission_controller

router = APIRouter()


@router.get("/get-all", response_model=List[Submission])
def submissions_list():
    return submission_controller.get_all_submissions()


@router.get("/get-one/{submission_id}", response_model=SubmissionFull)
def submission_get_one(submission_id: int):
    return submission_controller.get_submission_by_id(submission_id)


@router.post("/create", response_model=SubmissionFull)
def create_submission(submission_data: SubmissionCreate):
    return submission_controller.create_submission(submission_data)


@router.delete("/delete-submission/{submission_id}")
def delete_submission(submission_id: int):
    return submission_controller.delete_submission(submission_id)


@router.patch("/evaluate/{submission_id}", response_model=SubmissionFull)
def submission_evaluate(submission_id: int, evaluation: int):
    return submission_controller.evaluate_submission(evaluation, submission_id)

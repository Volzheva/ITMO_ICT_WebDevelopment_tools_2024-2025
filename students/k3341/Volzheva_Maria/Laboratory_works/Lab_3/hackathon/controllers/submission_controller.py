from fastapi import Depends, HTTPException
from sqlmodel import select
from typing import List

from hackathon.db import get_session
from hackathon.models import Submission, SubmissionFull, SubmissionCreate, MemberTeamLink
from hackathon.auth import auth_handler


def get_all_submissions(session=Depends(get_session)) -> List[Submission]:
    return session.exec(select(Submission)).all()


def get_submission_by_id(submission_id: int, session=Depends(get_session)) -> SubmissionFull:
    return session.get(Submission, submission_id)


def create_submission(
    submission_data: SubmissionCreate,
    authUserId=Depends(auth_handler.get_user),
    session=Depends(get_session)
) -> SubmissionFull:
    auth_member_team_link = session.scalars(select(MemberTeamLink).where(
        MemberTeamLink.team_id == submission_data.team_id,
        MemberTeamLink.user_id == authUserId
    )).first()
    if auth_member_team_link is None:
        raise HTTPException(status_code=403, detail="User not available")

    submission_model = Submission.model_validate(submission_data)
    session.add(submission_model)
    session.commit()
    session.refresh(submission_model)
    return submission_model


def delete_submission(
    submission_id: int,
    authUserId=Depends(auth_handler.get_user),
    session=Depends(get_session)
):
    submission = session.get(Submission, submission_id)
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")

    auth_member_team_link = session.scalars(select(MemberTeamLink).where(
        MemberTeamLink.team_id == submission.team_id,
        MemberTeamLink.user_id == authUserId
    )).first()
    if auth_member_team_link is None:
        raise HTTPException(status_code=403, detail="User not available")

    session.delete(submission)
    session.commit()
    return {"ok": True}


def evaluate_submission(
    evaluation: int,
    submission_id: int,
    authUserId=Depends(auth_handler.get_user),
    session=Depends(get_session)
) -> SubmissionFull:
    submission = session.get(Submission, submission_id)
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")

    auth_member_team_link = session.scalars(select(MemberTeamLink).where(
        MemberTeamLink.team_id == submission.team_id,
        MemberTeamLink.user_id == authUserId
    )).first()
    if auth_member_team_link is None:
        raise HTTPException(status_code=403, detail="User not available")

    submission.evaluation = evaluation
    session.add(submission)
    session.commit()
    session.refresh(submission)
    return submission

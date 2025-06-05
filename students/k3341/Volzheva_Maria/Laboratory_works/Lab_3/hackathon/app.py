from fastapi import FastAPI
from .db import *
from .routing.user_router import router as user_router
from .routing.hackathon_router import router as hackathon_router
from .routing.team_router import router as team_router
from .routing.task_router import router as task_router
from .routing.submission_router import router as submission_router
from .routing.parser_router import router as parse_router
app = FastAPI(debug=True)


app.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(team_router, prefix="/team", tags=["team"])
app.include_router(hackathon_router, prefix="/hackathon", tags=["hackathon"])
app.include_router(task_router, prefix="/task", tags=["task"])
app.include_router(submission_router, prefix="/submission", tags=["submission"])
app.include_router(parse_router, prefix="/parse", tags=["parser"])


@app.on_event("startup")
def on_startup():
    init_db()
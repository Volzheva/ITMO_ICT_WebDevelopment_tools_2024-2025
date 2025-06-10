# Лабораторная работа 1. Реализация серверного приложения FastAPI

## Цель работы
Научится реализовывать полноценное серверное приложение с помощью фреймворка FastAPI с применением дополнительных средств и библиотек.

## Тема
Создание системы для проведения хакатонов

### Описание
Задача состоит в разработке программной системы, которая будет использоваться для организации и проведения хакатонов. Хакатон - это соревнование, на котором участники, как правило, программисты, дизайнеры и бизнес-специалисты, работают над проектами в течение определенного времени, решая поставленные задачи или разрабатывая новые идеи. 
Каждая программа должна содержать функцию `calculate_sum()`, которая будет выполнять вычисления. Для `threading` используйте модуль `threading`, для `multiprocessing` - модуль `multiprocessing`, а для `async` - ключевые слова `async/await` и модуль `asyncio`.

## Схема базы данных
![](db.png)

Файл models.py:
``` python
from enum import Enum
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
import datetime
import sqlmodel


class MemberTeamLink(SQLModel, table=True):
    team_id: int = Field(default=None, foreign_key="team.id", primary_key=True)
    user_id: int = Field(default=None, foreign_key="user.id", primary_key=True)
    role: str = Field(default="Member")
    team: "Team" = Relationship(back_populates="member_links")
    member: "User" = Relationship(back_populates="team_links")


class HackathonTeamLink(SQLModel, table=True):
    team_id: int = Field(default=None, foreign_key="team.id", primary_key=True)
    hackathon_id: int = Field(default=None, foreign_key="hackathon.id", primary_key=True)


class UserRole(Enum):
    admin = 'admin'
    user = 'user'


class UserAuth(SQLModel):
    username: str
    password: str


class UserUpdate(SQLModel):
    full_name: Optional[str] = Field(default=None)
    email: Optional[str] = Field(default=None)
    phone_number: Optional[str] = Field(default=None)
    password: Optional[str] = Field(default=None)


class UserPublic(SQLModel):
    id: int
    username: str
    full_name: Optional[str]
    email: Optional[str]
    phone_number: Optional[str]


class UserForTeam(UserPublic):
    member_role: str


class UserProfile(SQLModel):
    id: int
    username: str
    full_name: Optional[str]
    email: Optional[str]
    phone_number: Optional[str]
    role: UserRole = Field(default=UserRole.user)


class _UserModelBase(SQLModel):
    id: int = Field(default=None, primary_key=True)
    role: UserRole = Field(default=UserRole.user)
    username: str = Field(index=True, unique=True, nullable=False)
    password: str = Field(nullable=False)
    full_name: Optional[str] = Field(default=None)
    email: Optional[str] = Field(default=None)
    phone_number: Optional[str] = Field(default=None)


class User(_UserModelBase, table=True):
    team_links: Optional[List[MemberTeamLink]] = Relationship(back_populates="member", sa_relationship_kwargs={"cascade": "all, delete"})
    teams: Optional[List["Team"]]= Relationship(back_populates="members", link_model=MemberTeamLink, sa_relationship_kwargs={"cascade": "all, delete"})


class UserTeams(_UserModelBase):
    teams: Optional[List["Team"]] = None


class HackathonCreate(SQLModel):
    name: str
    start_date: datetime.datetime
    end_date: datetime.datetime
    description: Optional[str] = Field(default=None)


class HackathonUpdate(SQLModel):
    name: Optional[str] = Field(default=None)
    start_date: Optional[datetime.datetime] = Field(default=None)
    end_date: Optional[datetime.datetime] = Field(default=None)
    description: Optional[str] = Field(default=None)


class _HackathonModelBase(SQLModel):
    name: str = Field(nullable=False)
    start_date: datetime.datetime = Field(nullable=False)
    end_date: datetime.datetime = Field(nullable=False)
    description: Optional[str] = Field(default=None)


class Hackathon(_HackathonModelBase, table=True):
    id: int = Field(default=None, primary_key=True)
    teams: Optional[List["Team"]]= Relationship(back_populates="hackathons", link_model=HackathonTeamLink, sa_relationship_kwargs={"cascade": "all, delete"})
    tasks: List["Task"] = Relationship(
        back_populates="hackathon",
        sa_relationship_kwargs={
            "cascade": "all, delete",
        },
    )


class HackathonFull(_HackathonModelBase):
    teams: Optional[List["Team"]] = None
    tasks: Optional[List["Task"]] = None


class TeamCreate(SQLModel):
    name: str
    description: Optional[str] = Field(default=None)


class TeamUpdate(SQLModel):
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)


class _TeamModelBase(SQLModel):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    description: Optional[str] = Field(default=None)


class Team(_TeamModelBase, table=True):
    member_links: Optional[List[MemberTeamLink]] = Relationship(back_populates="team",
                                                              sa_relationship_kwargs={"cascade": "all, delete"})
    members: Optional[List["User"]] = Relationship(back_populates="teams", link_model=MemberTeamLink, sa_relationship_kwargs={"cascade": "all, delete"})
    hackathons: Optional[List["Hackathon"]] = Relationship(back_populates="teams", link_model=HackathonTeamLink, sa_relationship_kwargs={"cascade": "all, delete"})
    submissions: Optional[List["Submission"]] = Relationship(
        back_populates="team",
        sa_relationship_kwargs={
            "cascade": "all, delete",
        },
    )


class TeamFull(_TeamModelBase):
    hackathons: Optional[List["Hackathon"]] = None
    members: Optional[List["UserForTeam"]] = None
    submissions: Optional[List["Submission"]] = None


# Tasks

class TaskCreate(SQLModel):
    title: str = Field(nullable=False)
    hackathon_id: int = Field(foreign_key="hackathon.id")
    description: Optional[str] = Field(default=None)
    requirements: Optional[str] = Field(default=None)
    evaluation_criteria: Optional[str] = Field(default=None)


class TaskUpdate(SQLModel):
    title: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    requirements: Optional[str] = Field(default=None)
    evaluation_criteria: Optional[str] = Field(default=None)


class _TaskModelBase(SQLModel):
    id: int = Field(default=None, primary_key=True)
    title: str = Field(nullable=False)
    description: Optional[str] = Field(default=None)
    requirements: Optional[str] = Field(default=None)
    evaluation_criteria: Optional[str] = Field(default=None)
    hackathon_id: int = Field(foreign_key="hackathon.id")


class Task(_TaskModelBase, table=True):
    hackathon: "Hackathon" = Relationship(back_populates="tasks")
    submissions: List["Submission"] = Relationship(
        back_populates="task",
        sa_relationship_kwargs={
            "cascade": "all, delete",
        },
    )


class TaskFull(_TaskModelBase):
    hackathon: Optional["Hackathon"] = None
    submissions: Optional[List["Submission"]] = None



class SubmissionCreate(SQLModel):
    submission_data: str = Field(nullable=False)
    team_id: int = Field(foreign_key="team.id")
    task_id: int = Field(foreign_key="task.id")


class _SubmissionModelBase(SQLModel):
    id: int = Field(default=None, primary_key=True)
    submission_data: str = Field(nullable=False)
    evaluation: Optional[int] = Field(default=None)
    team_id: int = Field(foreign_key="team.id")
    task_id: int = Field(foreign_key="task.id")


class Submission(_SubmissionModelBase, table=True):
    team: "Team" = Relationship(back_populates="submissions")
    task: "Task" = Relationship(back_populates="submissions")


class SubmissionFull(_SubmissionModelBase):
    team: Optional["Team"] = None
    task: Optional["Task"] = None


class UserCreate(SQLModel):
    username: str
    password: str
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    role: UserRole = Field(default=UserRole.user)
```

## Подключеник к базе данных
Файл database.py:
```python
import os
from sqlmodel import SQLModel, Session, create_engine
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv("DB_ADMIN")
if not db_url:
    raise ValueError("Переменная окружения DB_ADMIN не задана")

engine = create_engine(db_url, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
```

Файл .env:
```
DB_ADMIN = postgresql://postgres:postgres@localhost/lab1web
LAB1_JWT_KEY=supersecretkey1234567890
LAB1_ADMIN_KEY=masha
```

## Реализованные end-points
![](endpoits_1.PNG)
![](endpoits_2.PNG)

## Запуск программы
```
 python -m uvicorn main:app --reload

```

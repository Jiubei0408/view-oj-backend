from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.models.base import Base


class User(UserMixin, Base):
    __tablename__ = 'user'

    username = Column(String(100), primary_key=True)
    nickname = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    permission = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False)
    oj_username = relationship("app.models.entity.OJUsername", back_populates="user")
    accept_problem = relationship("app.models.entity.AcceptProblem")

    def get_id(self):
        return self.username


class Problem(Base):
    __tablename__ = 'problem'

    id = Column(Integer, primary_key=True, autoincrement=True)
    oj_id = Column(Integer, ForeignKey('oj.id'))
    oj = relationship("app.models.entity.OJ")
    problem_pid = Column(String(100), nullable=False)
    rating = Column(Integer, nullable=False)


class AcceptProblem(Base):
    __tablename__ = 'accept_problem'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), ForeignKey('user.username'))
    problem_id = Column(Integer, ForeignKey('problem.id'))
    problem = relationship("app.models.entity.Problem")
    add_rating = Column(Integer, nullable=False)
    create_time = Column(DateTime, nullable=False)


class OJ(Base):
    __tablename__ = 'oj'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True)
    status = Column(Integer, nullable=False)


class OJUsername(Base):
    __tablename__ = 'oj_username'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), ForeignKey('user.username'))
    user = relationship("app.models.entity.User", back_populates="oj_username")
    oj_id = Column(Integer, ForeignKey('oj.id'))
    oj = relationship("app.models.entity.OJ")
    oj_username = Column(String(100), nullable=False)


class Task(Base):
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True, autoincrement=True)
    task_name = Column(String(100), nullable=False)
    kwargs = Column(String(100), nullable=False)
    status = Column(Integer, nullable=False)
    create_time = Column(DateTime, nullable=False)
    start_time = Column(DateTime)
    finish_time = Column(DateTime)

from sqlalchemy import Column, Integer, String, ForeignKey, Table, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

user_test = Table(
    "user_resolved_test",
    Base.metadata,
    Column("user_id", String, ForeignKey("user_t.telegram_id")),
    Column("test_id", Integer, ForeignKey("test.id")),
)


class Test(Base):
    __tablename__ = "test"
    id = Column(Integer, primary_key=True)
    spreadsheet_id = Column(String)
    author_id = Column(String, ForeignKey("user_t.telegram_id"))
    author = relationship("User", back_populates="tests", foreign_keys=[author_id])
    users = relationship("User", secondary=user_test, back_populates="resolved_tests", uselist=True)
    questions = relationship("Question", back_populates="test", uselist=True)
    sessions = relationship("Session", back_populates="test", uselist=True)


class User(Base):
    __tablename__ = "user_t"
    id = Column(Integer, primary_key=True)
    telegram_id = Column(String, nullable=False, unique=True, index=True)
    resolved_tests = relationship("Test", secondary=user_test, back_populates="users")
    tests = relationship("Test", back_populates="author")
    answers = relationship("Answer", back_populates="user")
    session = relationship("Session", back_populates="user", uselist=False)


class Session(Base):
    __tablename__ = "session"
    id = Column(Integer, primary_key=True)
    user_id = Column(String, ForeignKey("user_t.telegram_id"))
    user = relationship("User", back_populates="session")
    test_id = Column(Integer, ForeignKey("test.id"))
    test = relationship("Test", back_populates="sessions")
    question_num = Column(Integer)


class Question(Base):
    __tablename__ = "question"
    text = Column(String)
    id = Column(Integer, primary_key=True)
    test_id = Column(Integer, ForeignKey("test.id"))
    test = relationship("Test", back_populates="questions")
    options = relationship("Option", back_populates="question", uselist=True)
    answers = relationship("Answer", back_populates="question", uselist=True)


class Option(Base):
    __tablename__ = "option"
    text = Column(String)
    correct = Column(Boolean)
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey("question.id"))
    question = relationship("Question", back_populates="options")
    answers = relationship("Answer", back_populates="option", uselist=True)


class Answer(Base):
    __tablename__ = "answer"
    text = Column(String)
    id = Column(Integer, primary_key=True)
    user_id = Column(String, ForeignKey("user_t.telegram_id"))
    user = relationship("User", back_populates="answers", uselist=False)
    option_id = Column(Integer, ForeignKey("option.id"))
    option = relationship("Option", back_populates="answers", uselist=False)
    question_id = Column(Integer, ForeignKey("question.id"))
    question = relationship("Question", back_populates="answers")

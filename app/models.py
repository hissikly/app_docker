from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from database import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)
    question_text = Column(String, nullable=False, index=True)
    
class Choice(Base):
    __tablename__ = "choices"

    id = Column(Integer, primary_key=True)
    choice_text = Column(String, index=True)
    is_correct = Column(Boolean, nullable=False, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"))
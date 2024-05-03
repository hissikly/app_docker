from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException
from models import Question, Choice
from sqlalchemy.orm import Session
import schemas as schemas
from database import engine, Base, SessionLocal
from typing import List

app = FastAPI()
Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/")
def main():
    return {"message": "Hello world"}


@app.post("/create-quiz", response_model=schemas.QuestionCreate)
def create_quiz(new_quiz: schemas.QuestionCreate, session: db_dependency):
    question = session.query(Question).filter(Question.question_text == new_quiz.question_text).first()
    if question:
        raise HTTPException(status_code=400, detail="question is already registered")
    
    new_question = Question(question_text=new_quiz.question_text)
    session.add(new_question)
    session.commit()
    session.refresh(new_question)

    for choice in new_quiz.choices:
        new_choice = Choice(choice_text=choice.choice_text, is_correct=choice.is_correct, question_id=new_question.id)
        session.add(new_choice)
    session.commit()
    raise HTTPException(status_code=200, detail="success")


@app.get("/read-question/{question_id}", response_model=schemas.QuestionBase)
def read_question(question_id: int, session: Session = Depends(get_db)):
    question = session.query(Question).filter(Question.id == question_id).first()
    session.commit()
    if not question:
        raise HTTPException(status_code=404, detail="not found")
    return question

@app.get("/read-choice/{choice_id}", response_model=List[schemas.ChoiceBase])
def  read_choice(choice_id: int, session: Session = Depends(get_db)):
    choice = session.query(Choice).filter(Choice.question_id == choice_id).all()
    session.commit()
    if not choice:
        raise HTTPException(status_code=404, detail="not found")
    return choice
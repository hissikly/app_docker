from pydantic import BaseModel, ConfigDict
from typing import List

class QuestionBase(BaseModel):
    question_text: str

    model_config = ConfigDict(arbitrary_types_allowed=True)

class ChoiceBase(BaseModel):
    choice_text: str
    is_correct: bool

    model_config = ConfigDict(arbitrary_types_allowed=True)

class QuestionCreate(BaseModel):
    question_text: str
    choices: List[ChoiceBase]
    
    model_config = ConfigDict(arbitrary_types_allowed=True)

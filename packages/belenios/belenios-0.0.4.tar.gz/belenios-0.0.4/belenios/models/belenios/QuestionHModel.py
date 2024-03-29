from sqlalchemy import Column, Integer, ForeignKey

from belenios.custom_types.belenios.BType import BType
from belenios.custom_types.belenios.IType import IType
from belenios.models.belenios.QuestionModel import QuestionModel


class QuestionHModel(QuestionModel):
    id = Column(Integer, ForeignKey('question_model.id'), primary_key=True)
    min = Column(IType, nullable=False)
    max = Column(IType, nullable=False)
    blank = Column(BType, nullable=False)
    __mapper_args__ = {
        "polymorphic_identity": "QuestionHModel",
    }

    # Override constructor to set 'type' to 'NonHomomorphic'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = 'QuestionHModel'

    def __str__(self):
        return (
            f"QuestionHModel(\n"
            f"    id={self.id},\n"
            f"    min={self.min},\n"
            f"    max={self.max},\n"
            f"    blank={self.blank},\n"
            f"    type={self.type},\n"
            f"    question={self.question},\n"
            f"    answers={self.answers},\n"
            f"    extra={self.extra}\n"
            f")"
        )
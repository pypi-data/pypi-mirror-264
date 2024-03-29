from sqlalchemy import Column, Integer, ForeignKey

from belenios.models.belenios.QuestionModel import QuestionModel


class QuestionNhModel(QuestionModel):
    id = Column(Integer, ForeignKey('question_model.id'), primary_key=True)
    __mapper_args__ = {
        "polymorphic_identity": "QuestionNhModel",
    }

    # Override constructor to set 'type' to 'Homomorphic'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = 'QuestionNhModel'

    def __str__(self):
        return (
            f"QuestionNhModel(\n"
            f"    id={self.id},\n"
            f"    type={self.type},\n"
            f"    question={self.question},\n"
            f"    answers={self.answers},\n"
            f"    extra={self.extra}\n"
            f")"
        )
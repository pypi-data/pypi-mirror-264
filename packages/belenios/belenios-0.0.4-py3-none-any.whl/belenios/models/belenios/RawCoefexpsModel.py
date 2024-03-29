from sqlalchemy import Column, Integer, ForeignKey

from belenios.custom_types.belenios.ArrayOfGsType import ArrayOfGsType
from belenios.models.belenios.SignedObjectModel import SignedObjectModel


class RawCoefexpsModel(SignedObjectModel):
    id = Column(Integer, ForeignKey('signed_object_model.id'), primary_key=True)
    raw_coefexps = Column(ArrayOfGsType, nullable=False)
    __mapper_args__ = {
        "polymorphic_identity": "RawCoefexpsModel",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = 'RawCoefexpsModel'

    def __str__(self):
        return (
            f"RawCoefexpsModel(\n"
            f"    raw_coefexps={self.raw_coefexps}\n"
            f")"
        )
    def to_json(self):
        return {
            "raw_coefexps": self.raw_coefexps,
        }

    @staticmethod
    def load_from_json(dict):
        return RawCoefexpsModel(type=dict['type'], raw_coefexps=dict['raw_coefexps'])

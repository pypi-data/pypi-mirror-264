from belenios.custom_types.belenios.StringType import StringType

from sqlalchemy import Column, Integer, ForeignKey

from belenios.models.belenios.SignedObjectModel import SignedObjectModel
from sqlalchemy import Column, Integer, ForeignKey

from belenios.custom_types.belenios.StringType import StringType
from belenios.models.belenios.SignedObjectModel import SignedObjectModel


class SignedStringModel(SignedObjectModel):
    id = Column(Integer, ForeignKey('signed_object_model.id'), primary_key=True)
    value = Column(StringType, nullable=False)
    __mapper_args__ = {
        "polymorphic_identity": "SignedStringModel",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = 'SignedStringModel'

    def __str__(self):
        return (
            f"SignedStringModel(\n"
            f"    value={self.value}\n"
            f")"
        )

    def to_json(self):
        return {
            "value": self.value,
        }

    @staticmethod
    def load_from_json(dict):
        return SignedStringModel(type=dict['type'], value=dict['value'])

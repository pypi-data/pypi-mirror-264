from sqlalchemy import Column, Integer, ForeignKey

from belenios.custom_types.belenios.GType import GType
from belenios.models.belenios.SignedObjectModel import SignedObjectModel


class CertKeysModel(SignedObjectModel):
    id = Column(Integer, ForeignKey('signed_object_model.id'), primary_key=True)
    verification = Column(GType)
    encryption = Column(GType)
    __mapper_args__ = {
        "polymorphic_identity": "CertKeysModel",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = 'CertKeysModel'

    def __str__(self):
        return (
            f"CertKeysModel(\n"
            f"    verification={self.verification},\n"
            f"    encryption={self.encryption}\n"
            f")"
        )
    def to_json(self):
        return {
            "verification": self.verification,
            "encryption": self.encryption,
        }
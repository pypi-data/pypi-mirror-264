from sqlalchemy import Column

from belenios.custom_types.belenios.StringType import StringType
from belenios.models.BaseModel import BaseModel


class SetupDataModel(BaseModel):
    election = Column(StringType, nullable=True)
    trustees = Column(StringType, nullable=True)
    credentials = Column(StringType, nullable=True)

    def __str__(self):
        return (
            f"SetupDataModel(\n"
            f"    election={self.election},\n"
            f"    trustees={self.trustees},\n"
            f"    credentials={self.credentials}\n"
            f")"
        )
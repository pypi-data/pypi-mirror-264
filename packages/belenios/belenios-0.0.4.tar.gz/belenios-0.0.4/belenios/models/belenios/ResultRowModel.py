from sqlalchemy import Column
from sqlalchemy import Integer, ForeignKey

from belenios.custom_types.belenios.ArrayOfIsType import ArrayOfIsType
from belenios.models.BaseModel import BaseModel


class ResultRowModel(BaseModel):
    result_id = Column(Integer, ForeignKey('result_model.id'))
    result_cells = Column(ArrayOfIsType, nullable=False)

    def __init__(self, *args, **kwargs):
        if 'result_cells' not in kwargs:
            kwargs['result_cells'] = []
        super().__init__(*args, **kwargs)

    def __str__(self):
        return (
            f"ResultRowModel(\n"
            f"    result_id={self.result_id},\n"
            f"    result_cells={self.result_cells},\n"
            f")"
        )
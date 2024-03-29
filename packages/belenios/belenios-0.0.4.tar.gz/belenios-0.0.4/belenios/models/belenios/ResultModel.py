from typing import List

from sqlalchemy import Column
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from belenios.models.BaseModel import BaseModel
from belenios.models.belenios.ResultRowModel import ResultRowModel


class ResultModel(BaseModel):
    result_rows: Mapped[List[ResultRowModel]] = relationship("ResultRowModel", uselist=True,
                                                             cascade="all, delete-orphan",
                                                             single_parent=True)

    def __str__(self):
        result_rows_info = ', '.join(str(result_row) for result_row in self.result_rows)
        return (
            f"ResultModel(\n"
            f"    result_rows=[{result_rows_info}]\n"
            f")"
        )
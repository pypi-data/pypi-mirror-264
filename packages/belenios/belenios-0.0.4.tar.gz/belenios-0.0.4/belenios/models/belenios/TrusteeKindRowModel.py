# from typing import List
#
# from sqlalchemy import Column
# from sqlalchemy import Integer, ForeignKey
# from sqlalchemy.orm import relationship, Mapped
#
# from belenios.models.BaseModel import BaseModel
# from belenios.models.belenios.TrusteeKindModel import TrusteeKindModel
#
#
# class TrusteeKindRowModel(BaseModel):
#     election_bundle_id = Column(Integer, ForeignKey('election_bundle_model.id'), nullable=False)
#     trustee_kinds: Mapped[List[TrusteeKindModel]] = relationship('TrusteeKindModel', uselist=True,
#                                                                  cascade="all, delete-orphan",
#                                                                  single_parent=True)
#
#     def __init__(self, *args, **kwargs):
#         if 'trustee_kinds' not in kwargs:
#             kwargs['trustee_kinds'] = []
#         super().__init__(*args, **kwargs)

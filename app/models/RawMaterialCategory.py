from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from ..database import Base

class RawMaterialCategory(Base):
    __tablename__ = 'raw_material_category'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), index=True, unique=True, nullable=False)
    active = Column(Boolean, default=True)

    # Relationships
    raw_materials = relationship('RawMaterial', back_populates='category')
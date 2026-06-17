from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database.postgres import Base

class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    transport_score = Column(Float, default=0.0)
    energy_score = Column(Float, default=0.0)
    waste_score = Column(Float, default=0.0)
    total_co2 = Column(Float, default=0.0)  # in kg CO2e
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="assessments")
    recommendations = relationship("Recommendation", back_populates="assessment")
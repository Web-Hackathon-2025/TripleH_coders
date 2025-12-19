from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    provider_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String, index=True)
    description = Column(String)
    category = Column(String, index=True)
    price = Column(Float)
    location = Column(String) # Simple string for now, could be lat/lng
    
    provider = relationship("User", back_populates="services")
    bookings = relationship("Booking", back_populates="service")

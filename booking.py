from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database import Base
import enum
from datetime import datetime

class BookingStatus(str, enum.Enum):
    REQUESTED = "REQUESTED"
    CONFIRMED = "CONFIRMED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    REJECTED = "REJECTED"

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("users.id"))
    service_id = Column(Integer, ForeignKey("services.id"))
    status = Column(Enum(BookingStatus), default=BookingStatus.REQUESTED)
    scheduled_time = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    customer = relationship("User", back_populates="bookings_as_customer", foreign_keys=[customer_id])
    service = relationship("Service", back_populates="bookings")

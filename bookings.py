from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas import BookingCreate, BookingSchema
from app.models.booking import Booking, BookingStatus
from app.models.service import Service
from app.models.user import User, UserRole
from app import auth

router = APIRouter(prefix="/bookings", tags=["bookings"])

@router.post("/", response_model=BookingSchema)
def create_booking(
    booking: BookingCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(auth.get_current_user)
):
    if current_user.role != UserRole.CUSTOMER:
        raise HTTPException(status_code=403, detail="Only customers can book services")
    
    service = db.query(Service).filter(Service.id == booking.service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
        
    new_booking = Booking(
        customer_id=current_user.id,
        service_id=booking.service_id,
        scheduled_time=booking.scheduled_time,
        status=BookingStatus.REQUESTED
    )
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking

@router.get("/", response_model=List[BookingSchema])
def get_my_bookings(db: Session = Depends(get_db), current_user: User = Depends(auth.get_current_user)):
    if current_user.role == UserRole.CUSTOMER:
        return db.query(Booking).filter(Booking.customer_id == current_user.id).all()
    elif current_user.role == UserRole.PROVIDER:
        # Join with Service to find bookings for my services
        return db.query(Booking).join(Service).filter(Service.provider_id == current_user.id).all()
    return []

@router.patch("/{booking_id}/status", response_model=BookingSchema)
def update_booking_status(
    booking_id: int, 
    status: BookingStatus, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(auth.get_current_user)
):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
        
    # Permission logic:
    # Provider can Accept/Reject/Complete
    # Customer can Cancel
    # Simple logic for now:
    
    is_provider = booking.service.provider_id == current_user.id
    is_customer = booking.customer_id == current_user.id
    
    if not (is_provider or is_customer):
        raise HTTPException(status_code=403, detail="Not authorized")
        
    booking.status = status
    db.commit()
    db.refresh(booking)
    return booking

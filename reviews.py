from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from pydantic import BaseModel
from datetime import datetime
from app.models.review import Review
from app.models.booking import Booking, BookingStatus
from app.models.user import User, UserRole
from app import auth

router = APIRouter(prefix="/reviews", tags=["reviews"])

class ReviewCreate(BaseModel):
    booking_id: int
    rating: int
    comment: str

class ReviewSchema(BaseModel):
    id: int
    booking_id: int
    rating: int
    comment: str
    created_at: datetime
    
    class Config:
        from_attributes = True

@router.post("/", response_model=ReviewSchema)
def create_review(
    review: ReviewCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(auth.get_current_user)
):
    # Only customer can review
    if current_user.role != UserRole.CUSTOMER:
        raise HTTPException(status_code=403, detail="Only customers can leave reviews")
        
    booking = db.query(Booking).filter(Booking.id == review.booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
        
    if booking.customer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your booking")
        
    if booking.status != BookingStatus.COMPLETED:
        raise HTTPException(status_code=400, detail="Can only review completed bookings")
        
    new_review = Review(
        booking_id=review.booking_id,
        rating=review.rating,
        comment=review.comment
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review

@router.get("/", response_model=List[ReviewSchema])
def get_reviews(service_id: int, db: Session = Depends(get_db)):
    # Get reviews for a specific service (via bookings)
    return db.query(Review).join(Booking).filter(Booking.service_id == service_id).all()

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.schemas import ServiceCreate, ServiceSchema
from app.models.service import Service
from app.models.user import User, UserRole
from app import auth

router = APIRouter(prefix="/services", tags=["services"])

@router.get("/", response_model=List[ServiceSchema])
def get_services(
    search: Optional[str] = None, 
    category: Optional[str] = None, 
    db: Session = Depends(get_db)
):
    query = db.query(Service)
    if search:
        query = query.filter(Service.title.contains(search) | Service.description.contains(search))
    if category:
        query = query.filter(Service.category == category)
    return query.all()

@router.post("/", response_model=ServiceSchema)
def create_service(
    service: ServiceCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(auth.get_current_user)
):
    if current_user.role != UserRole.PROVIDER:
        raise HTTPException(status_code=403, detail="Only providers can create services")
    
    new_service = Service(**service.dict(), provider_id=current_user.id)
    db.add(new_service)
    db.commit()
    db.refresh(new_service)
    return new_service

@router.get("/{service_id}", response_model=ServiceSchema)
def get_service(service_id: int, db: Session = Depends(get_db)):
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service

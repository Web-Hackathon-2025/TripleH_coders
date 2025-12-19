from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import auth, services, bookings, reviews

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Karigar API", description="Hyperlocal Services Marketplace API", version="0.1.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(services.router)
app.include_router(bookings.router)
app.include_router(reviews.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Karigar API"}

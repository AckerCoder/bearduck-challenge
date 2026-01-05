"""
Main FastAPI application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine, get_db, Base
from routes import products, cart, orders
from controllers.products import init_sample_products

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="E-commerce API",
    description="Full-stack e-commerce challenge API",
    version="1.0.0"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(products.router)
app.include_router(cart.router)
app.include_router(orders.router)


@app.on_event("startup")
async def startup_event():
    """Initialize database with sample data on startup"""
    db = next(get_db())
    init_sample_products(db)
    db.close()


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "E-commerce API is running",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.get("/health")
def health():
    """Health check endpoint"""
    return {"status": "healthy"}

# shortener_app/main.py
import secrets

import validators
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


def get_db():
    """Dependency to get a SQLAlchemy database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def raise_bad_request(message):
    """
    Raise an HTTPException with a 400 status code
    and the provided error message.
    """
    raise HTTPException(status_code=400, detail=message)


def raise_not_found(request):
    """
    Raise an HTTPException with a 404 status code and a message
    indicating that the requested URL doesn't exist.
    """
    message = f"URL '{request.url}' doesn't exist"
    raise HTTPException(status_code=404, detail=message)


@app.get("/")
def read_root():
    """Welcome message for the API."""
    return "Welcome to the URL shortener API"


@app.post("/url", response_model=schemas.URLInfo)
def create_url(url: schemas.URLBase, db: Session = Depends(get_db)):
    """Create a new shortened URL."""
    if not validators.url(url.target_url):
        raise_bad_request(message="Your provided url is not valid")

    db_url = crud.create_db_url(db=db, url=url)
    db_url.url = db_url.key
    db_url.admin_url = db_url.secret_key

    return db_url


@app.get("/{url_key}")
def forward_to_target_url(
    url_key: str, request: Request, db: Session = Depends(get_db)
):
    """Redirect to the target URL for the specified shortened URL key."""
    if db_url := crud.get_db_url_by_key(db=db, url_key=url_key):
        return RedirectResponse(db_url.target_url)
    else:
        raise_not_found(request)

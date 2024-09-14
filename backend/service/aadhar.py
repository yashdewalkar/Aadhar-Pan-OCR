from sqlalchemy.orm import Session

from ..schemas import aadhar as aadharSchema
from ..models import aadhar as aadharModel
from fastapi import HTTPException,status


def get_all(db: Session):
    aadhars = db.query(aadharModel.Aadhar).all()
    return aadhars

def create(request: aadharModel.Aadhar,db: Session, get_user):
    request.user_id = get_user
    new_aadhar = aadharModel.Aadhar(**request.dict())
    db.add(new_aadhar)
    db.commit()
    db.refresh(new_aadhar)
    return new_aadhar

def destroy(id:int,db: Session):
    aadhar = db.query(aadharModel.Aadhar).filter(aadharModel.Aadhar.id == id)

    if not aadhar.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Aadhar with id {id} not found")

    aadhar.delete(synchronize_session=False)
    db.commit()
    return 'done'


def update(id: int, request: aadharModel.Aadhar, db: Session):
    Aadhar = db.query(aadharModel.Aadhar).filter(aadharModel.Aadhar.id == id).first()

    if not Aadhar:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Aadhar with id {id} not found")

    # Update the Aadhar object with the properties from the request
    for attr, value in request.dict().items():
        setattr(Aadhar, attr, value)

    db.commit()
    return 'updated'


def show(id:int,db:Session):
    aadhar = db.query(aadharModel.Aadhar).filter(aadharModel.Aadhar.id == id).first()
    if not aadhar:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Aadhar with the id {id} is not available")
    return aadhar
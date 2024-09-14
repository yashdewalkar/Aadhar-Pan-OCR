from sqlalchemy.orm import Session

from ..schemas import pan as panSchema
from ..models import pan as panModel
from fastapi import HTTPException,status


def get_all(db: Session):
    pans = db.query(panModel.Pan).all()
    return pans

def create(request: panModel.Pan,db: Session, get_user):
    request.user_id = get_user
    new_pan = panModel.Pan(**request.dict())
    db.add(new_pan)
    db.commit()
    db.refresh(new_pan)
    return new_pan

def destroy(id:int,db: Session):
    pan = db.query(panModel.Pan).filter(panModel.Pan.id == id)

    if not pan.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"pan with id {id} not found")

    pan.delete(synchronize_session=False)
    db.commit()
    return 'done'


def update(id: int, request: panModel.Pan, db: Session):
    pan = db.query(panModel.Pan).filter(panModel.Pan.id == id).first()

    if not pan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"pan with id {id} not found")

    # Update the pan object with the properties from the request
    for attr, value in request.dict().items():
        setattr(pan, attr, value)

    db.commit()
    return 'updated'


def show(id:int,db:Session):
    pan = db.query(panModel.Pan).filter(panModel.Pan.id == id).first()
    if not pan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"pan with the id {id} is not available")
    return pan
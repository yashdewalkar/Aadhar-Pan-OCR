from typing import List
from fastapi import APIRouter,Depends,status,HTTPException
from ..utils import oauth2
from ..utils import token

from ..schemas import pan as panSchema
from ..schemas import user as userSchema

from ..database import database
from sqlalchemy.orm import Session
from ..service import pan as panService
from fastapi import APIRouter, UploadFile, File

import pytesseract
from PIL import Image
import os, json , re



router = APIRouter(
    prefix="/pan",
    tags=['Pan'],
    dependencies=[Depends(oauth2.get_current_user)]
) 

get_db = database.get_db

@router.post('/upload', status_code=status.HTTP_201_CREATED)
async def upload_pan_photo(file: UploadFile = File(...)):
    # Save the uploaded file
    file_path = f"assets/uploads/{file.filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # Perform OCR on the image
    img = Image.open(file_path)
    ocr_text = pytesseract.image_to_string(img)

    # split the OCR text into lines and remove any empty lines
    ocr_lines = list(filter(None, ocr_text.split('\n')))

       ## getting the pan number
    pan_number = re.search(r'[A-Z]{5}[0-9]{4}[A-Z]{1}', ocr_text).group()
    print(pan_number)

    # find the line containing the name using regex
    father_name = None
    name = None
    dob = None

    for i in range(len(ocr_lines)):
        if "Father's Name" in ocr_lines[i]:
            father_name = ocr_lines[i+1]
            ocr_lines.pop(i)
            ocr_lines.pop(i+1)
            break

    

    for i in range(len(ocr_lines)):
        if "Name" in ocr_lines[i]:
            name = ocr_lines[i+1]
            break
    
    for text in ocr_lines:
        match = re.search(r'\b(\d{2}/\d{2}/\d{4})\b', text)
        if match:
            dob = match.group(1)
            break
    

    data = { 'pan_number': pan_number.strip() , 'name': name.strip() ,  'father_name': father_name.strip(), 'dob': dob.strip() }
    
    os.remove(file_path)

    # return the OCR text
    return data
    #return json.dumps(data)

    

@router.get('/', response_model=List[panSchema.ShowPan])
def all(db: Session = Depends(get_db) , get_user = Depends(oauth2.get_user) ):
    print(get_user)
    return panService.get_all(db)


@router.post('/', status_code=status.HTTP_201_CREATED,)
def create(request: panSchema.Pan, db: Session = Depends(get_db) , get_user = Depends(oauth2.get_user)):
    return panService.create(request, db, get_user)

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id:int, db: Session = Depends(get_db)):
    return panService.destroy(id,db)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id:int, request: panSchema.Pan, db: Session = Depends(get_db)):
    return panService.update(id,request, db)


@router.get('/{id}', status_code=200, response_model=panSchema.ShowPan)
def show(id:int, db: Session = Depends(get_db)):
    return panService.show(id,db)

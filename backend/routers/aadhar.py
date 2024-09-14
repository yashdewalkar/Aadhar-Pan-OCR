from typing import List
from fastapi import APIRouter,Depends,status,HTTPException
from ..utils import oauth2
from ..utils import token

from ..schemas import aadhar as aadharSchema
from ..schemas import user as userSchema

from ..database import database
from sqlalchemy.orm import Session
from ..service import aadhar as aadharService
from fastapi import APIRouter, UploadFile, File

import pytesseract
from PIL import Image
import os, json , re



router = APIRouter(
    prefix="/aadhar",
    tags=['Aadhar'],
    dependencies=[Depends(oauth2.get_current_user)]
) 

get_db = database.get_db

@router.post('/upload', status_code=status.HTTP_201_CREATED)
async def upload_aadhar_photo(file: UploadFile = File(...)):
    # Save the uploaded file
    file_path = f"assets/uploads/{file.filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # Perform OCR on the image
    img = Image.open(file_path)
    ocr_text = pytesseract.image_to_string(img)

    # split the OCR text into lines and remove any empty lines
    ocr_lines = list(filter(None, ocr_text.split('\n')))

    # find the line containing the name using regex
    name_regex = re.compile(r'[A-Z][a-z]* [A-Z][a-z]*([ ][A-Z][a-z]*)*')
    name_line = next((line for line in ocr_lines if name_regex.match(line)), None)

    # extract the name using regex
    name = re.search(name_regex, name_line).group()

    print(name)


    pattern = r'Male|Female|MALE|FEMALE'
    matches = re.findall(pattern, ocr_text)
    gender = matches[0]

    
    ## getting the dob
    dob_match = re.search(r'DOB : \s*(\d{2}/\d{2}/\d{4})', ocr_text)
    yob_match = re.search(r'Year of Birth - \s*(\d{4})', ocr_text)
    
    if dob_match:
        dob = dob_match.group(1)
        print(dob)
    elif yob_match:
        yob = yob_match.group(1)
        dob = yob
    else:
        dob = ''

    print(dob)


    ## getting the aadhar number
    aadhar_number = re.search(r'(\d{4}\s\d{4}\s\d{4})', ocr_text).group(1)
    print(aadhar_number)

    data = {'name': name.strip(), 'dob': dob.strip(), 'gender': gender.strip(), 'aadhar_number': aadhar_number.strip()}
    
    os.remove(file_path)

    # return the OCR text
    return data
    #return json.dumps(data)

    

@router.get('/', response_model=List[aadharSchema.ShowAadhar])
def all(db: Session = Depends(get_db) , get_user = Depends(oauth2.get_user) ):
    print(get_user)
    return aadharService.get_all(db)


@router.post('/', status_code=status.HTTP_201_CREATED,)
def create(request: aadharSchema.Aadhar, db: Session = Depends(get_db) , get_user = Depends(oauth2.get_user)):
    return aadharService.create(request, db, get_user)

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id:int, db: Session = Depends(get_db)):
    return aadharService.destroy(id,db)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id:int, request: aadharSchema.Aadhar, db: Session = Depends(get_db)):
    return aadharService.update(id,request, db)


@router.get('/{id}', status_code=200, response_model=aadharSchema.ShowAadhar)
def show(id:int, db: Session = Depends(get_db)):
    return aadharService.show(id,db)

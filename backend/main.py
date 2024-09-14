from fastapi import FastAPI
from .models.common import run_migration
from .routers import blog, user,authentication,aadhar,pan

app = FastAPI(
    title="Validation of Aadhar & Pan Car using OCR",
    description=open("assets/description/project_description.txt").read()
)

run_migration()
     
app.include_router(authentication.router)
#app.include_router(blog.router)
app.include_router(user.router)
app.include_router(aadhar.router)
app.include_router(pan.router)  

 
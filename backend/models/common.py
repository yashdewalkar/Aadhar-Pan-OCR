from ..database.database import engine
from . import blog,user,aadhar, pan

def run_migration():
    blog.Base.metadata.create_all(engine)
    user.Base.metadata.create_all(engine)  
    aadhar.Base.metadata.create_all(engine)   
    pan.Base.metadata.create_all(engine) 
from App.models import Recruiter
from App.database import db
from sqlalchemy.exc import IntegrityError



def create_recruiter(username,password,email):
    try:
        newRecruiter = Recruiter(username,password,email)
        db.session.add(newRecruiter)
        db.session.commit()
        return True
    except IntegrityError:
        db.session.rollback()
        return False    
    

def list_created_jobs(recruiter_id):
    recruiter = Recruiter.query.get(recruiter_id)   

    if recruiter:
        for job in recruiter.jobs:
            print(f'{job}')
    else:
     print("The recruiter does not exist") 





    
    
    
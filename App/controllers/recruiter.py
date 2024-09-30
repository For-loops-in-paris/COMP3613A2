from App.models import Recruiter
from App.database import db


def create_recruiter(username,password,company_name):
    newRecruiter = Recruiter(username,password,company_name)
    db.session.add(newRecruiter)
    db.session.commit()
    
    

def list_created_jobs(recruiter_id):
    recruiter = Recruiter.query.get(recruiter_id)   

    if recruiter:
        for job in recruiter.jobs:
            print(f'{job}')
    else:
     print("The recruiter does not exist") 





    
    
    
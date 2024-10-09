from App.database import db
from App.models import Job
from App.models import Application
from App.models import Recruiter
from sqlalchemy.exc import IntegrityError

def create_job(recruiter_id,position, salary):
   
    #Verifies that the recruiter id is a valid digit and converts it to an integer
    if not recruiter_id or not position or not salary:
        return False
    
    if isinstance(salary,str):
        if salary.isdigit():
            salary = int(salary)
    else:
        return False
    if isinstance(recruiter_id,str):
        if recruiter_id.isdigit():
            recruiter_id = int(recruiter_id)
        else:
           print (f'Please enter a digit for the recruiter id')
           return False

    if not Recruiter.query.get(recruiter_id):
        print ('Please enter a valid recruiter id')
        return False
    
   
    try:
        job = Job(recruiter_id,position,salary)
        db.session.add(job)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        print(f'{position} job was not successfully created')
        return False
    print(f'{position} job was successfully created!')
    return True

def view_applicants(job_id):

    job = Job.query.get(job_id)
    if job:
        if not job.applicants:
            print(f'There are no applicants for the {job.position}')
        for applicant in job.applicants:
            print(applicant)
    else:
        print('No job exists with the specified id')


from App.database import db
from App.models import Job
from App.models import Application
from App.models import Recruiter
from sqlalchemy.exc import IntegrityError

def create_job(recruiter_id,position, salary):
   
    #Verifies that the recruiter id is a valid digit and converts it to an integer
    if isinstance(recruiter_id,str):
        if recruiter_id.isdigit():
            recruiter_id = int(recruiter_id)
        else:
            return f'Please enter a digit for the recruiter id'

    if not Recruiter.query.get(recruiter_id):
        return 'Please enter a valid recruiter id'
    
    try:
        job = Job(recruiter_id,position,salary)
        db.session.add(job)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return f'{position} job was not successfully created'
    return f'{position} job was successfully created!'

def view_applicants(job_id):

    job = Job.query.get(job_id)
    if job:
        if not job.applicants:
            print(f'There are no applicants for the {job.position}')
        for applicant in job.applicants:
            print(applicant)
    else:
        print('No job exists with the specified id')


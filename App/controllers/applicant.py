from App.database import db
from .application import create_application
from App.models import Job
from App.models import Applicant
from sqlalchemy.exc import IntegrityError

def create_applicant(username,password,first_name,last_name,phone_number,email_address):
    try:
        newApplicant = Applicant(username,password,first_name,last_name,phone_number,email_address)
        db.session.add(newApplicant)
        db.session.commit()
        print(f'Applicant {first_name} {last_name} was successfuly created')
        return True
    except IntegrityError:
        print( f'Applicant {first_name} {last_name} could not be created')
        return False


def view_jobs():
    jobs = Job.query.all()
    for job in jobs:
        print(job)

def apply_to_job(job_id,applicant_id):
    application = create_application(job_id,applicant_id)
    if application:
        return 'Application successful'
    return "Either the application already exists, the user is not an applicant, or the application couldn't be made"

def view_applications(applicant_id):
    applicant = Applicant.query.get(applicant_id)
    
    if applicant:
        for application in applicant.applications:
            print(application)
    else:
        print("FAIL")


    


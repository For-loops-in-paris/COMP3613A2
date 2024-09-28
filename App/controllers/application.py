from App.models import Application
from App.models import Applicant
from App.models import Job
from sqlalchemy.exc import IntegrityError


from App.database import db

def create_application(job_id,applicant_id):
    if Job.query.get(job_id) and Applicant.query.get(applicant_id):
        return False
    try:
        application = Application(job_id,applicant_id)
        db.session.add(application)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return False
    return True


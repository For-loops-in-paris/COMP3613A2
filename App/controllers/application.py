from App.models import Application, Applicant,Job
from sqlalchemy.exc import IntegrityError


from App.database import db

def create_application(job_id,applicant_id):
    
    if Application.query.filter_by(job_id=job_id,applicant_id=applicant_id).first() != None:
        return False
        
    if not Applicant.query.get(applicant_id):
        return False
    try:
        application = Application(job_id,applicant_id)
        db.session.add(application)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return False
    return True

# def list_all_applications():
#     app = Application.query.all()
#     for a in app:
#         print(a)

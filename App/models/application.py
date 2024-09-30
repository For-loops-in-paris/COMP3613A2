from App.database import db
from .user import User
from datetime import datetime

class Application(db.Model):    
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'))
    applicant_id = db.Column(db.Integer, db.ForeignKey('applicant.id'),nullable=False)
    application_date = db.Column(db.DateTime,default=datetime.now())
    application_status = db.Column(db.Boolean)

    def __init__(self,job_id,applicant_id):
        self.job_id = job_id
        self.applicant_id = applicant_id
    

    def __repr__(self):
        return f'Applicant id: {self.applicant_id} Job ID: {self.job_id} Status = {self.application_status} Date = {(self.application_date).strftime("%Y-%m-%d %H:%M:%S")}'
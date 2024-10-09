from App.database import db

class Job(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.String(120), nullable=False)
    recruiter_id= db.Column(db.Integer,db.ForeignKey('recruiter.id'))
    salary = db.Column(db.Integer,nullable=False)
    

    def __init__(self,recruiter_id,position,salary):
        self.recruiter_id = recruiter_id
        self.position = position
        self.salary = salary

    def __repr__(self):
        return f'Job ID: {self.id} Company: {self.recruiter.company.company_name} Position: {self.position} Salary: {self.salary}'
     

    
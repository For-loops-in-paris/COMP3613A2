from App.database import db

class Job(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.String(120), nullable=False)
    recruiter_id= db.Column(db.Integer,db.ForeignKey('recruiter.id'))
    description = db.Column(db.Text,nullable=False)
    salary = db.Column(db.Integer,nullable=False)
    

    def __init__(self,recruiter_id,position,description,salary):
        self.recruiter_id = recruiter_id
        self.position = position
        self.description = description
        self.salary = salary

    def get_json(self):
        return {
            "company":self.recruiter.company.company_name,
            "position":self.position,
            "salary": self.salary
        }
    
    def __repr__(self):
        return f'Job ID: {self.id} Company: {self.recruiter.company.company_name} Position: {self.position} Salary: {self.salary}'
     

    
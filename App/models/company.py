from App.database import db

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(120), nullable=False)
    company_logo =  db.Column(db.String(120), nullable=False)
    recruiters = db.relationship('Recruiter',backref="company")

    def __init__(self,company_name,company_logo):
        self.company_name = company_name
        self.company_logo = company_logo

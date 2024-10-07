from App.database import db

from .user import User

class Recruiter(User):
    id = db.Column(db.Integer,db.ForeignKey('user.id'),primary_key=True)
    company_id = db.Column(db.Integer,db.ForeignKey('company.id'))
    jobs = db.relationship('Job',backref="recruiter" )

    __mapper_args__ = {
        'polymorphic_identity': 'recruiter'
    }

    def __init__(self, username,password,email):
        super().__init__(username, password,email)

    def __repr__(self):
        return f'Username: {self.username} Company: {self.company.company_name}'

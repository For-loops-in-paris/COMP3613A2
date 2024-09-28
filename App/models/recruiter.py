from App.database import db

from .user import User

class Recruiter(User):
    id = db.Column(db.Integer,db.ForeignKey('user.id'),primary_key=True)
    company_name = db.Column(db.String(120), nullable=False)
    jobs = db.relationship('Job',backref="recruiter" )

    __mapper_args__ = {
        'polymorphic_identity': 'recruiter'
    }

    def __init__(self, username,password,company_name):
        super().__init__(username, password)
        self.company_name = company_name
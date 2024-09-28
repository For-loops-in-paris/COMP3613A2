from .user import create_user
from .recruiter import create_recruiter
from .job import create_job
from .applicant import create_applicant
from App.database import db


def initialize():
    db.drop_all()
    db.create_all()
    create_recruiter('Carl','Carlpass','Google')
    create_recruiter('Rickyy23','Rickpass','Amazon')
    create_applicant('Johnboy123','Johnpass','John','Doe',413-2242,'john@mail.com')
    create_applicant('Paulboy123','Paulpass','Paul','Doe',413-2242,'paul@mail.com')
    create_applicant('Jeanboy123','Rickpass','Jean','Doe',413-2242,'jean@mail.com')
    create_applicant('Suzieboy123','Suziepass','Suzie','Doe',413-2242,'suzie@mail.com')
    create_job(1,'Plumber',2520)
    create_job(1,'Tinkerer',2520)
    create_job(2,'Masseus',2520)
    

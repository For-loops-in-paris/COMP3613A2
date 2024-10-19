from .user import create_user
from .recruiter import create_recruiter
from .job import create_job
from .applicant import create_applicant
from .company import create_company
from .admin import create_admin, assign_recruiter
from App.database import db


def initialize():
    db.drop_all()
    db.create_all()
    create_admin("bob","bobpass","bob@mail.com")
    create_company('Google','https://cdn2.hubspot.net/hubfs/53/image8-2.jpg')
    create_company('Amazon','https://www.hatchwise.com/wp-content/uploads/2022/05/amazon-logo-1024x683.png')
    create_recruiter('Carl','Carlpass','carl@mail.com')
    create_recruiter('Rickyy23','Rickpass','ricky@mail.com')
    assign_recruiter(2,1)
    assign_recruiter(3,2)
    create_applicant('Johnboy123','Johnpass','John','Doe',413-2242,'john@mail.com')
    create_applicant('Paulboy123','Paulpass','Paul','Doe',413-2242,'paul@mail.com')
    create_applicant('Jeanboy123','Rickpass','Jean','Doe',413-2242,'jean@mail.com')
    create_applicant('Suzieboy123','Suziepass','Suzie','Doe',413-2242,'suzie@mail.com')
    create_job(1,'Plumber',"Fixes Pipes",2520)
    create_job(1,'Tinkerer',"Manipulates objects",2520)

    create_job(3,'Masseus',"Massages People",2520)
    

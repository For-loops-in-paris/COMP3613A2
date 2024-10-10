from App.models import Admin
from App.models import Company
from App.models import Recruiter

from App.database import db


from sqlalchemy.exc import IntegrityError
from App.database import db

def create_admin(username,password,email):
    try:
        newAdmin = Admin( username,password,email)
        db.session.add(newAdmin)
        db.session.commit()
        return True
    except IntegrityError:
        db.session.rollback()
        return False

def assign_recruiter(recruiter_id,company_id):
    company = Company.query.get(company_id)
    recruiter = Recruiter.query.get(recruiter_id)
    if company and recruiter:
        recruiter.company_id=company_id
        company.recruiters.append(recruiter)
        db.session.commit()
        print(recruiter)
    else:
        print("Either the recruiter id or company id is invalid")
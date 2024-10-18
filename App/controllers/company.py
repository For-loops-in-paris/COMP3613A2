from App.models import Company
from sqlalchemy.exc import IntegrityError
from App.database import db

def create_company(company_name,company_logo):
    try:
        newCompany = Company(company_name,company_logo)
        db.session.add(newCompany)
        db.session.commit()
        return True
    except IntegrityError:
        db.session.rollback()
        return False

def get_company(company_id):
    return Company.query.get(company_id)

def list_company_jobs_json(company_id):
    li =[]
    company = Company.query.get(company_id)
    if company:
        for r in company.recruiters:
            print(r.username)
            for job in r.jobs:
                li.append(job.get_json())
    return li


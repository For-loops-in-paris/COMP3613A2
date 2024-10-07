from App.models import Company
from sqlalchemy.exc import IntegrityError
from App.database import db

def create_company(company_name,company_logo):
    try:
        newCompany = Company(company_name,company_logo)
        db.session.add(newCompany)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()


import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import *
from App.controllers import (
    create_user,
    create_admin,
    create_company,
    create_recruiter,
    assign_recruiter,
    create_applicant,
    create_job,
    get_job,
    get_company,
    view_jobs_json,
    view_applicants_json,
    apply_to_job,
    withdraw_application,
    get_user_by_username
)


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_new_user(self):
        user = User("bob", "bobpass","bob@mail.com")
        assert user.username == "bob"

    # pure function no side effects or integrations called
    def test_get_json(self):
        user = User("bob", "bobpass","bob@mail.com")
        user_json = user.get_json()
        self.assertDictEqual(user_json, {"id":None, "username":"bob"})
    
    def test_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password, method='sha256')
        user = User("bob", password,"bob@mail.com")
        assert user.password != password

    def test_check_password(self):
        password = "mypass"
        user = User("bob", password,"bob@mail.com")
        assert user.check_password(password)

    def test_new_admin(self):
        admin = Admin("bob", "bobpass","bob@mail.com")
        assert admin.username == "bob"

    def test_new_applicant(self):
        applicant = Applicant("BarryAllen", "Barrypass","Barry","Allen","314-1989","bob@mail.com")
        assert applicant.username == "BarryAllen"

    def test_new_recruiter(self):
        recruiter = Recruiter("Lebron", "lebronpass","lebron@james.com")
        assert recruiter.username == "Lebron"

    def test_new_company(self):
        company = Company("Google","https://cdn2.hubspot.net/hubfs/53/image8-2.jpg")
        assert company.company_name == "Google"

    def test_new_job(self):
        job = Job(1,"JuniorDev","Develops things juniorly",9999)
        assert job.position == "JuniorDev"

    def test_new_application(self):
        application = Application(1,1)
        assert application.job_id == 1

    

'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()


class UsersIntegrationTests(unittest.TestCase):

    def test_01_create_user(self): #ID IS 1
        user = create_user("ross", "rosspass", "ross@mail.com")
        new_user = get_user_by_username("ross")
        assert new_user.username == "ross" and new_user.email_address == "ross@mail.com"
        
    def test_02_create_admin(self): # ID IS 2
        admin = create_admin("bob", "bobpass", "bob@mail.com")
        new_admin = get_user_by_username("bob")
        assert new_admin.username == "bob" and new_admin.email_address == "bob@mail.com"
    
    def test_03_create_company(self): # ID IS 1
        create_company('Google','https://cdn2.hubspot.net/hubfs/53/image8-2.jpg')
        new_company = get_company(1)
        assert new_company.company_name == "Google" and new_company.company_logo == "https://cdn2.hubspot.net/hubfs/53/image8-2.jpg"

    def test_04_create_recruiter(self): # ID IS 3
        create_recruiter("rick", "rickpass","rick@mail.com")
        recruiter = get_user_by_username('rick')
        assert recruiter.username == "rick" and recruiter.email_address == "rick@mail.com"
        
    def test_05_assign_recruiter(self):
        admin = get_user_by_username("bob")
        company = get_company(1)
        recruiter = get_user_by_username('rick')
        assign_recruiter(3, 1)
        assert recruiter.company_id == 1
        
    def test_06_create_applicant(self): # ID IS 4
        create_applicant("BruceWayne", "brucepass", "Bruce", "Wayne", "456-9535", "bruce@wayne.com")
        applicant = get_user_by_username("BruceWayne")
        assert applicant.username == "BruceWayne" and applicant.first_name == "Bruce" and applicant.last_name == "Wayne" and applicant.phone_number == "456-9535" and applicant.email_address == "bruce@wayne.com"

    def test_07_create_job(self): # ID IS 1
        recruiter = get_user_by_username('rick')
        create_job(recruiter.id, "JuniorDev", "Develops things juniorly", 999)
        new_job = get_job(1)
        assert new_job.recruiter_id == recruiter.id and new_job.position == "JuniorDev" and new_job.description == "Develops things juniorly" and new_job.salary == 999
        
    def test_08_view_jobs_json(self):
        recruiter = get_user_by_username('rick')
        create_job(recruiter.id, "SeniorDev", "Develops things seniorly", 444)
        jobs = view_jobs_json()
        expected_jobs = [
        {"company": recruiter.company.company_name, "position": "JuniorDev", "salary": 999},
        {"company": recruiter.company.company_name, "position": "SeniorDev", "salary": 444}
        ]
        self.assertListEqual(expected_jobs, jobs)
    
    def test_09_apply_to_job(self):
        job = get_job(1)
        applicant = get_user_by_username("BruceWayne")
        apply_msg = apply_to_job(job.id, applicant.id)
        assert apply_msg == "Application successful"
        
    def test_10_view_applicants_json(self):
        job = get_job(1)
        applicants_json = view_applicants_json(job.id)
        expected_applicants = [{"id": 4, "username": "BruceWayne"}]
        self.assertListEqual(expected_applicants, applicants_json)
        
    def test_11_withdraw_application(self):
        job = get_job(1)
        applicant = get_user_by_username("BruceWayne")
        applicants_before_withdraw = view_applicants_json(job.id)
        assert {"id": applicant.id, "username": applicant.username} in applicants_before_withdraw
        withdraw_result = withdraw_application(job.id, applicant.id)
        assert withdraw_result == True
        applicants_after_withdraw = view_applicants_json(job.id)
        assert {"id": applicant.id, "username": applicant.username} not in applicants_after_withdraw
        
    def test_12_job_get_json(self):
        new_job = get_job(1)
        job_json = new_job.get_json()
        expected_job_json = {"company": "Google", "position": "JuniorDev", "salary": 999}
        self.assertDictEqual(expected_job_json, job_json)
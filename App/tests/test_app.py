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
    get_all_users_json,
    login,
    get_user,
    get_user_by_username,
    update_user
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
        assert new_user.username == "ross"
        
    def test_02_create_admin(self): # ID IS 2
        admin = create_admin("bob", "bobpass", "bob@mail.com")
        new_admin = get_user_by_username("bob")
        assert new_admin.username == "bob"
    
    def test_03_create_company(self): # ID IS 1
        create_company('Google','https://cdn2.hubspot.net/hubfs/53/image8-2.jpg')
        new_company = get_company(1)
        assert new_company.company_name == "Google"

    def test_04_create_recruiter(self): # ID IS 3
        create_recruiter("rick", "rickpass","rick@mail.com")
        recruiter = get_user_by_username('rick')
        assert recruiter.username == "rick"
        
    def test_05_assign_recruiter(self):
        admin = get_user_by_username("bob")
        company = get_company(1)
        recruiter = get_user_by_username('rick')
        assign_recruiter(3, 1)
        assert recruiter.company_id == 1
        
    def test_06_create_applicant(self): # ID IS 4
        create_applicant("BruceWayne", "brucepass", "Bruce", "Wayne", 456-9535, "bruce@wayne.com")
        applicant = get_user_by_username("BruceWayne")
        assert applicant.username == "BruceWayne"

    def test_07_create_job(self): # ID IS 1
        recruiter = get_user_by_username('rick')
        create_job(recruiter.id, "JuniorDev", "Develops things juniorly", 999)
        new_job = get_job(1)
        assert new_job.position == "JuniorDev"
        
    def test_08_view_jobs_json(self):
        recruiter = get_user_by_username('rick')
        create_job(recruiter.id, "SeniorDev", "Develops things seniorly", 444)
        jobs = view_jobs_json()
        expected_jobs = [
        {"company": recruiter.company.company_name, "position": "JuniorDev", "salary": 999},
        {"company": recruiter.company.company_name, "position": "SeniorDev", "salary": 444}
        ]
        self.assertListEqual(expected_jobs, jobs)
    
    def _test_09_apply_to_job(self):
        new_job = get_job(1)
        applicant = get_user_by_username("BruceWayne")
        apply_msg = apply_to_job(new_job.id, applicant.id)
        print(apply_msg)
        assert applicant.id == 9
        
    def test_10_view_applicants_json(self):
        new_job = get_job(1)
        applicants_json = view_applicants_json(new_job.id)
        expected_applicants = [{"id": 4, "username": "BruceWayne"}]
        self.assertListEqual(expected_applicants, applicants_json)
        
    #def test_11_withdraw_application(self):
     #   new_job = get_job(1)
      #  applicant = get_user_by_username("BruceWayne")
       # withdraw_result = withdraw_application(1, 4)
        #assert withdraw_result == True
        
    def test_12_job_get_json(self):
        new_job = get_job(1)
        job_json = new_job.get_json()
        expected_job_json = {"company": "Google", "position": "JuniorDev", "salary": 999}
        self.assertDictEqual(expected_job_json, job_json)
import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import *
from App.controllers import (
    create_user,
    create_recruiter,
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


def test_authenticate():
    user = create_user("bob", "bobpass","bob@mail.com")
    assert login("bob", "bobpass","bob@mail.com") != None

class UsersIntegrationTests(unittest.TestCase):

    def test_create_user(self):
        user = create_user("rick", "bobpass")
        assert user.username == "rick"

    def test_create_recruiter(self):
        create_recruiter("rick", "bobpass","bob@mail.com")
        recruiter = get_user_by_username('rick')
        assert recruiter.username == "rick"

    def test_get_all_users_json(self):
        users_json = get_all_users_json()
        self.assertListEqual([{"id":1, "username":"bob"}, {"id":2, "username":"rick"}], users_json)

    # Tests data changes in the database
    def test_update_user(self):
        update_user(1, "ronnie")
        user = get_user(1)
        assert user.username == "ronnie"
        


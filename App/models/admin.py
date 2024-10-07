from App.database import db
from .user import User


class Admin(User):

    __mapper_args__ = {
        'polymorphic_identity': 'admin'
    }
    id = db.Column(db.Integer,db.ForeignKey('user.id'),primary_key=True)

    def __init__(self, username, password, email):
        super().__init__(username, password, email)

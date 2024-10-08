from flask_login import login_user, login_manager, logout_user, LoginManager, current_user
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity, verify_jwt_in_request
from flask import render_template


from functools import wraps
from App.models import User, Applicant, Recruiter, Admin

def login(username, password):
  user = User.query.filter_by(username=username).first()
  if user and user.check_password(password):
    return create_access_token(identity=username)
  return None

def setup_flask_login(app):
    login_manager = LoginManager()
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        user = Admin.query.get(user_id)

        if user:
            return user
        
        user = Recruiter.query.get(user_id)

        if user:
            return user

        return Applicant.query.get(user_id)
    
    return login_manager

def setup_jwt(app):
  jwt = JWTManager(app)

  # configure's flask jwt to resolve get_current_identity() to the corresponding user's ID
  @jwt.user_identity_loader
  def user_identity_lookup(identity):
    user = Admin.query.filter_by(username=identity).one_or_none()
    if user:
        return user.id
    
    user = Recruiter.query.filter_by(username=identity).one_or_none()
    if user:
        return user.id
    
    user = Applicant.query.filter_by(username=identity).one_or_none()
    if user:
        return user.id
    return None

  @jwt.user_lookup_loader
  def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.get(identity)

  return jwt

#wrappers 
def applicant_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not isinstance(current_user, Applicant):
            return render_template("401.html"), 401
        return func(*args, **kwargs)
    return wrapper

def recruiter_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not isinstance(current_user, Recruiter):
            return render_template("401.html"), 401
        return func(*args, **kwargs)
    return wrapper

# Context processor to make 'is_authenticated' available to all templates
def add_auth_context(app):
  @app.context_processor
  def inject_user():
      try:
          verify_jwt_in_request()
          user_id = get_jwt_identity()
          current_user = Admin.query.get(user_id)
          if not current_user:
            current_user = Recruiter.query.get(user_id)
          if not current_user:
            current_user = Applicant.query.get(user_id)
          is_authenticated = True
      except Exception as e:
          print(e)
          is_authenticated = False
          current_user = None
      return dict(is_authenticated=is_authenticated, current_user=current_user)
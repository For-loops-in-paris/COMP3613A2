from flask import Blueprint, render_template, jsonify, request, flash, send_from_directory, flash, redirect, url_for
from flask_login import login_user, login_manager, logout_user, LoginManager, current_user
from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies
from App.controllers.auth import recruiter_required


from App.controllers import(
    create_job
)

recruiter_views = Blueprint('recruiter_views', __name__, template_folder='../templates')


@recruiter_views.route('/create_job',methods=['GET'])
# @recruiter_required
def create_job_page():
    test = create_job()

@recruiter_views.route('/create_job',methods=['POST'])
# @recruiter_required
def create_job_action():
    data = request.json
    job = create_job(data['recruiter_id'],data['position'],data['salary'])
    if job:
        return jsonify({"message":"Job created successfully"}), 201
    else:
        return jsonify({"message":"Job creation failed"}), 400
   
from flask import Blueprint, render_template, jsonify, request, flash, send_from_directory, flash, redirect, url_for
from flask_login import login_user, login_manager, logout_user, LoginManager, current_user
from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies
from App.controllers.auth import applicant_required

from App.controllers import(
    create_application,
    withdraw_application,
    view_jobs_json,
    apply_to_job,
    view_applications_json,
    create_applicant,
    delete_applicant
)

applicant_views = Blueprint('applicant_views', __name__, template_folder='../templates')

 
@applicant_views.route('/view_jobs', methods=['GET'])
def view_job_listings():
    print("asd")
    return jsonify(view_jobs_json()), 200


@applicant_views.route('/create_application', methods=['POST'])
@applicant_required
def create_application_action():
    data=request.json
    application = create_application(data['job_id'], data['applicant_id'])
    if application:
        return jsonify({"message":"Application created successfully"}), 201
    else:
        return jsonify({"message":"Application creation failed"}), 400
    
@applicant_views.route('/create_applicant',methods=['POST'])
# @recruiter_required
def create_applicant_action():
    data = request.json 
    if len (data)!= 6:
        return jsonify({"message":"Applicant creation failed"}), 400
    applicant = create_applicant(data['username'],data['password'],data['first_name'],data['last_name'],data['phone_number'],data['email'])
    if applicant:
        return jsonify({"message":"Applicant created successfully"}), 201
    else:
        return jsonify({"message":"Applicant creation failed"}), 400
    

@applicant_views.route('/delete_applicant',methods=['DELETE'])
@applicant_required
def delete_applicant_action():
    data = request.json 
    if len (data)!= 1:
        return jsonify({"message":"Applicant deletion failed"}), 400
    recruiter = delete_applicant(data['applicant_id'])
    if recruiter:
        return jsonify({"message":"Applicant deleted successfully"}), 201
    else:
        return jsonify({"message":"Applicant deletion failed"}), 400
    
@applicant_views.route('/withdraw_application', methods=['DELETE'])
@applicant_required
def withdraw_application_action():
    data=request.json
    if withdraw_application(data['job_id'], data['applicant_id']):
        return jsonify({"message":"Application deleted successfully"}), 200
    else:
        return jsonify({"message":"Application delete failed"}), 400
    

@applicant_views.route('/view_applications', methods=['GET'])
def view_applications_listings():
    data=request.json
    return jsonify(view_applications_json(data['applicant_id'])), 200
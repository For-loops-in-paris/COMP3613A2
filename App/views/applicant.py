from flask import Blueprint, render_template, jsonify, request, flash, send_from_directory, flash, redirect, url_for
from flask_login import login_user, login_manager, logout_user, LoginManager, current_user
from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies
from App.controllers.auth import applicant_required

from App.controllers import(
    create_application,
    withdraw_application,
    view_jobs_json
)

applicant_views = Blueprint('applicant_views', __name__, template_folder='../templates')

 
@applicant_views.route('/view_jobs', methods=['GET'])
def view_job_listings():
    print("asd")
    return jsonify(view_jobs_json()), 200


@applicant_views.route('/create_application', methods=['POST'])
def create_application_action():
    data=request.json
    application = create_application(data['job_id'], data['applicant_id'])
    if application:
        return jsonify({"message":"Application created successfully"}), 201
    else:
        return jsonify({"message":"Application creation failed"}), 400
    

@applicant_views.route('/withdraw_application', methods=['DELETE'])
def withdraw_application_action():
    data=request.json
    if withdraw_application(data['job_id'], data['applicant_id']):
        return jsonify({"message":"Application deleted successfully"}), 200
    else:
        return jsonify({"message":"Application delete failed"}), 400
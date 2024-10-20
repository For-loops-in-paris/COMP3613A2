from flask import Blueprint, render_template, jsonify, request, flash, send_from_directory, flash, redirect, url_for
from flask_login import login_user, login_manager, logout_user, LoginManager, current_user
from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies
from App.controllers.auth import recruiter_required, admin_required



from App.controllers import(
    create_job, 
    create_recruiter,
    view_applicants_json,
    list_company_jobs_json,
    get_recruiter,
    delete_recruiter
    
)

recruiter_views = Blueprint('recruiter_views', __name__, template_folder='../templates')


# @recruiter_views.route('/create_job',methods=['GET'])
# # @recruiter_required
# def create_job_page():
#     test = create_job()

@recruiter_views.route('/create_job',methods=['POST'])
@recruiter_required
@jwt_required()
def create_job_action():
    data = request.json
    if len (data)!= 4:
        return jsonify({"message":"Job creation failed"}), 400
    job = create_job(data['recruiter_id'],data['position'],data['description'],data['salary'])
    if job:
        return jsonify({"message":"Job created successfully"}), 201
    else:
        return jsonify({"message":"Job creation failed"}), 400  
    

@recruiter_views.route('/create_recruiter',methods=['POST'])
# @recruiter_required
def create_recruiter_action():
    data = request.json 
    if len (data)!= 3:
        return jsonify({"message":"Recruiter creation failed"}), 400
    recruiter = create_recruiter(data['username'],data['password'],data['email'])
    if recruiter:
        return jsonify({"message":"Recruiter created successfully"}), 201
    else:
        return jsonify({"message":"Recruiter creation failed"}), 400
    

@recruiter_views.route('/delete_recruiter',methods=['DELETE'])
@recruiter_required
def delete_recruiter_action():
    data = request.json 
    if len (data)!= 1:
        return jsonify({"message":"Recruiter deletion failed"}), 400
    recruiter = delete_recruiter(data['recruiter_id'])
    if recruiter:
        return jsonify({"message":"Recruiter deleted successfully"}), 201
    else:
        return jsonify({"message":"Recruiter deletion failed"}), 400
    

@recruiter_views.route('/list_company_jobs',methods=['POST'])
@recruiter_required
def company_job_listings():
    data = request.json
    recruiter = get_recruiter(data['recruiter_id'])
    if len(data)!=1 or not recruiter:
        return jsonify(message='Company listing failed'),400
    
    return jsonify(list_company_jobs_json(recruiter.company_id)), 200
    

@recruiter_views.route('/list_applicants', methods=['GET'])
def view_applicant_listings():
    data=request.json
    print("asd")
    return jsonify(view_applicants_json(data['job_id'])), 200
    


    


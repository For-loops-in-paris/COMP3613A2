import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize, create_job , list_created_jobs,apply_to_job, view_jobs, view_applications, create_applicant, create_recruiter,view_applicants, )


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    print('d')
    create_user(username, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

'''
Recruiter Commands
'''
recruiter_cli = AppGroup('recruiter', help='recruiter object commands') 

@recruiter_cli.command('list_jobs')
@click.argument('recruiter_id')
def list_recruiter_jobs(recruiter_id):
    list_created_jobs(recruiter_id)

# @recruiter_cli.command('create_recruiter')
# @click.argument('username')
# @click.argument('password')
# @click.argument('company_name')
# def make_recruiter(company_name):
#     create_recruiter(company_name)
    
app.cli.add_command(recruiter_cli)

'''
Job Commands
'''
job_cli = AppGroup('job', help='job object commands') 

@job_cli.command('create_job')
@click.argument('recruiter_id')
@click.argument("position")
@click.argument("salary")
def create_new_job(recruiter_id,position,salary):
    print(create_job(recruiter_id,position,salary))
    
    
@job_cli.command('view_applicants')
@click.argument('job_id')
def list_applicants(job_id):
    view_applicants(job_id)
   

app.cli.add_command(job_cli)

'''
Applicant Commands
'''
applicant_cli = AppGroup('applicant', help='applicant object commands') 


@applicant_cli.command('apply_to_job')
@click.argument('job_id')
@click.argument('applicant_id')
def job_apply(job_id,applicant_id):
    print(apply_to_job(job_id,applicant_id))


@applicant_cli.command('view_jobs')
def job_listing():
    view_jobs()

@applicant_cli.command('view_applications')
@click.argument('applicant_id')
def list_applications(applicant_id):
    view_applications(applicant_id)


app.cli.add_command(applicant_cli)





'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)
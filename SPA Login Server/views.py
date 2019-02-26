from flask import render_template, flash, redirect, request, url_for, request
from app import app, db, models
import random
from datetime import datetime
import cryptutils

chal_username = ""
attempt = 0
chal = ""

def log(comment):
	timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
	log_filename = "/home/arj/Documents/spa_logs.txt"
	with open(log_filename, "a") as myfile:
		myfile.write(timestamp)
		myfile.write("       ")
		myfile.write(comment)
		myfile.write("   SPA1")
		myfile.write("\n")
	
def seperate_log():
	log_filename = "/home/arj/Documents/spa_logs.txt"
	with open(log_filename, "a") as myfile:
		myfile.write("--------------------------------------------------------------")
		myfile.write("\n")


# Checks if a username exists in the database
def user_exists(username):
	exists = db.session.query(models.User.id).filter_by(username=username).scalar() is not None
	return exists

def generate_chal(username):
	global chal_username
	chal_username = username
	return cryptutils.generate_chal(username)


# Returns svk for a specific username
def get_svk_for(username):
	svk = db.session.query(models.User.K).filter_by(username=username).first()
	return svk[0]


def verify_signature(svk, response, chal):
	global chal_username
	svk = get_svk_for(chal_username)
	return cryptutils.verify(svk, response, chal)




# Initial page for user study. Provides language choice
@app.route('/1/')
@app.route('/2/')
@app.route('/3/')
@app.route('/4/')
@app.route('/5/')
@app.route('/6/')
def init():
	user = request.path.split("/")[1]
	seperate_log()
	log("User study begins, get language selection page")
	return render_template('{}/init.html'.format(user))


# Login page
@app.route('/1/login')
@app.route('/2/login')
@app.route('/3/login')
@app.route('/4/login')
@app.route('/5/login')
@app.route('/6/login')
def login_page():
	user = request.path.split("/")[1]
	log("Get login page.")
	return render_template('{}/main.html'.format(user))

# Login page in turkish
@app.route('/1/tr/login')
@app.route('/2/tr/login')
@app.route('/3/tr/login')
@app.route('/4/tr/login')
@app.route('/5/tr/login')
@app.route('/6/tr/login')
def login_page_tr():
	user = request.path.split("/")[1]
	log("Get login page.")
	return render_template('{}/tr/main.html'.format(user))


# Registration page for POST requests. It accepts username and K and commits to the database.
@app.route('/1/register', methods=['POST'])
@app.route('/2/register', methods=['POST'])
@app.route('/3/register', methods=['POST'])
@app.route('/4/register', methods=['POST'])
@app.route('/5/register', methods=['POST'])
@app.route('/6/register', methods=['POST'])
@app.route('/1/tr/register', methods=['POST'])
@app.route('/2/tr/register', methods=['POST'])
@app.route('/3/tr/register', methods=['POST'])
@app.route('/4/tr/register', methods=['POST'])
@app.route('/5/tr/register', methods=['POST'])
@app.route('/6/tr/register', methods=['POST'])
def register_page():
	global attempt
	username = request.form['username']
	svk = request.form['K']
	log("Register posted. Username: {}, password: {}".format(username, svk))
	if user_exists(username):
		return "False"

	new_user = models.User(username=username, K=svk)
	db.session.add(new_user)
	db.session.commit()
	attempt = 0
	
	return "True"


# Authentication method. Gets username and K
@app.route('/1/auth', methods=['POST'])
@app.route('/2/auth', methods=['POST'])
@app.route('/3/auth', methods=['POST'])
@app.route('/4/auth', methods=['POST'])
@app.route('/5/auth', methods=['POST'])
@app.route('/6/auth', methods=['POST'])
@app.route('/1/tr/auth', methods=['POST'])
@app.route('/2/tr/auth', methods=['POST'])
@app.route('/3/tr/auth', methods=['POST'])
@app.route('/4/tr/auth', methods=['POST'])
@app.route('/5/tr/auth', methods=['POST'])
@app.route('/6/tr/auth', methods=['POST'])
def auth():
	global attempt
	global chal
	log("login posted")
	username = request.form['username']
	response = request.form['K']
	if user_exists(username):
		svk = get_svk_for(username)
		if verify_signature(svk, response, chal):
			attempt = 0
			return "True"
	
	attempt = attempt + 1
	return "False"



@app.route('/chal', methods=['POST'])
def send_chal():
	global chal
	username = request.form['username']
	chal = generate_chal(username)
	return chal



# Successful login page
@app.route('/1/login_success', methods=['GET'])
@app.route('/2/login_success', methods=['GET'])
@app.route('/3/login_success', methods=['GET'])
@app.route('/4/login_success', methods=['GET'])
@app.route('/5/login_success', methods=['GET'])
@app.route('/6/login_success', methods=['GET'])
def login_success_page():
	user = request.path.split("/")[1]
	log("Successful login")
	return render_template('{}/login_success.html'.format(user))


@app.route('/1/tr/login_success', methods=['GET'])
@app.route('/2/tr/login_success', methods=['GET'])
@app.route('/3/tr/login_success', methods=['GET'])
@app.route('/4/tr/login_success', methods=['GET'])
@app.route('/5/tr/login_success', methods=['GET'])
@app.route('/6/tr/login_success', methods=['GET'])
def login_success_page_tr():
	user = request.path.split("/")[1]
	log("Successful login")
	return render_template('{}/tr/login_success.html'.format(user))


# Fail login page
@app.route('/1/login_fail', methods=['GET'])
@app.route('/2/login_fail', methods=['GET'])
@app.route('/3/login_fail', methods=['GET'])
@app.route('/4/login_fail', methods=['GET'])
@app.route('/5/login_fail', methods=['GET'])
@app.route('/6/login_fail', methods=['GET'])
def login_fail_page():
	user = request.path.split("/")[1]
	global attempt
	log("Fail login")
	if attempt > 3:
		attempt = 0
		return render_template('{}/login_exit.html'.format(user))

	return render_template('{}/login_fail.html'.format(user))


# Fail login page
@app.route('/1/tr/login_fail', methods=['GET'])
@app.route('/2/tr/login_fail', methods=['GET'])
@app.route('/3/tr/login_fail', methods=['GET'])
@app.route('/4/tr/login_fail', methods=['GET'])
@app.route('/5/tr/login_fail', methods=['GET'])
@app.route('/6/tr/login_fail', methods=['GET'])
def login_fail_page_tr():
	user = request.path.split("/")[1]
	global attempt
	log("Fail login")
	if attempt > 3:
		return render_template('{}/tr/login_exit.html'.format(user))

	return render_template('{}/tr/login_fail.html'.format(user))


# Successful register page
@app.route('/1/register_success', methods=['GET'])
@app.route('/2/register_success', methods=['GET'])
@app.route('/3/register_success', methods=['GET'])
@app.route('/4/register_success', methods=['GET'])
@app.route('/5/register_success', methods=['GET'])
@app.route('/6/register_success', methods=['GET'])
def register_success_page():
	user = request.path.split("/")[1]
	log("Successful register")
	return render_template('{}/register_success.html'.format(user))




# Successful register page
@app.route('/1/tr/register_success', methods=['GET'])
@app.route('/2/tr/register_success', methods=['GET'])
@app.route('/3/tr/register_success', methods=['GET'])
@app.route('/4/tr/register_success', methods=['GET'])
@app.route('/5/tr/register_success', methods=['GET'])
@app.route('/6/tr/register_success', methods=['GET'])
def register_success_page_tr():
	user = request.path.split("/")[1]
	log("Successful register")
	return render_template('{}/tr/register_success.html'.format(user))




# Fail register page
@app.route('/1/register_fail', methods=['GET'])
@app.route('/2/register_fail', methods=['GET'])
@app.route('/3/register_fail', methods=['GET'])
@app.route('/4/register_fail', methods=['GET'])
@app.route('/5/register_fail', methods=['GET'])
@app.route('/6/register_fail', methods=['GET'])
def register_fail_page():
	user = request.path.split("/")[1]
	log("Fail register")
	return render_template('{}/register_fail.html'.format(user))


# Fail register page
@app.route('/1/tr/register_fail', methods=['GET'])
@app.route('/2/tr/register_fail', methods=['GET'])
@app.route('/3/tr/register_fail', methods=['GET'])
@app.route('/4/tr/register_fail', methods=['GET'])
@app.route('/5/tr/register_fail', methods=['GET'])
@app.route('/6/tr/register_fail', methods=['GET'])
def register_fail_page_tr():
	user = request.path.split("/")[1]
	log("Fail register")
	return render_template('{}/tr/register_fail.html'.format(user))




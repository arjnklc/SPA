from flask import render_template, flash, redirect, request, url_for, request
from app import app, db, models
import random
from datetime import datetime
import re



username = ""
attempt = 0


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

# Returns password for a specific username
def get_password_for(username):
	password = db.session.query(models.User.K).filter_by(username=username).first()
	return password[0]


def is_complex_password(password):
	specials = ".,:;!'^+%&/()=?_-<>"
	if re.search(r'[A-Z]', password) and re.search(r'[a-z]', password) and re.search(r'[0-9]', password) and any(char in specials for char in password) and len(password) > 7:
		return True

	return False


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
	log("User study begins, get language selection page. User: {}".format(user) )
	return render_template('{}/init.html'.format(user))


# Login page
@app.route('/1/login', methods=['GET'])
@app.route('/2/login', methods=['GET'])
@app.route('/3/login', methods=['GET'])
@app.route('/4/login', methods=['GET'])
@app.route('/5/login', methods=['GET'])
@app.route('/6/login', methods=['GET'])
@app.route('/1/tr/login', methods=['GET'])
@app.route('/2/tr/login', methods=['GET'])
@app.route('/3/tr/login', methods=['GET'])
@app.route('/4/tr/login', methods=['GET'])
@app.route('/5/tr/login', methods=['GET'])
@app.route('/6/tr/login', methods=['GET'])
def login_page():
	user = request.path.split("/")[1]
	log("Get login page.")
	if "/tr/" in request.path:
		return render_template('{}/tr/login.html'.format(user))

	return render_template('{}/login.html'.format(user))



# Register page
@app.route('/1/register', methods=['GET'])
@app.route('/2/register', methods=['GET'])
@app.route('/3/register', methods=['GET'])
@app.route('/4/register', methods=['GET'])
@app.route('/5/register', methods=['GET'])
@app.route('/6/register', methods=['GET'])
@app.route('/1/tr/register', methods=['GET'])
@app.route('/2/tr/register', methods=['GET'])
@app.route('/3/tr/register', methods=['GET'])
@app.route('/4/tr/register', methods=['GET'])
@app.route('/5/tr/register', methods=['GET'])
@app.route('/6/tr/register', methods=['GET'])
def register_page():
	user = request.path.split("/")[1]
	log("Get register page.")
	if "/tr/" in request.path:
		return render_template('{}/tr/register.html'.format(user))

	return render_template('{}/register.html'.format(user))




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
def register_post():
	user = request.path.split("/")[1]
	turkish = False
	if "/tr/" in request.path:
		turkish = True

	error = None
	inpt = request.form['username']
	inpt2 = request.form['password']
	inpt3 = request.form['password2']
	log("Register posted. Username: {} , Password: {}".format(inpt, inpt2))

	if user_exists(inpt):
		log("Register failed. Username is already taken.")
		if turkish:
			error = "Üyeliğiniz oluşturulamamıştır. Kullanıcı adı daha önce alınmış."
			return render_template("{}/tr/register.html".format(user), error=error)
		else:
			error = "Sign up is unsuccessful. Username is already taken!"
			return render_template("{}/register.html".format(user), error=error)

	elif inpt2 != inpt3:
		log("Register failed. Passwords do not match.")
		if turkish:
			error = "Üyeliğiniz oluşturulamamıştır. Parolalar uyuşmuyor."
			return render_template("{}/tr/register.html".format(user), error=error)
		else:
			error = "Sign up is unsuccessful. Passwords do not match, please try again."
			return render_template("{}/register.html".format(user), error=error)

	elif not is_complex_password(inpt2):
		log("Register failed. Weak password choice.")
		if turkish:
			error = "Üyeliğiniz oluşturulamamıştır. Zayıf parola."
			return render_template("{}/tr/register.html".format(user), error=error)
		else:
			error = "Sign up is unsuccessful. Weak Password."
			return render_template("{}/register.html".format(user), error=error)
	else:
		new_user = models.User(username=inpt, K=inpt2)
		db.session.add(new_user)
		db.session.commit()
		log("Register success.")
		if turkish:
			return render_template('{}/tr/register_success.html'.format(user))

		return render_template('{}/register_success.html'.format(user))



# Authentication method. Gets username and K
@app.route('/1/login', methods=['POST'])
@app.route('/2/login', methods=['POST'])
@app.route('/3/login', methods=['POST'])
@app.route('/4/login', methods=['POST'])
@app.route('/5/login', methods=['POST'])
@app.route('/6/login', methods=['POST'])
@app.route('/1/tr/login', methods=['POST'])
@app.route('/2/tr/login', methods=['POST'])
@app.route('/3/tr/login', methods=['POST'])
@app.route('/4/tr/login', methods=['POST'])
@app.route('/5/tr/login', methods=['POST'])
@app.route('/6/tr/login', methods=['POST'])
def login_post_page():
	global attempt
	user = request.path.split("/")[1]
	lang = ""
	if "/tr/" in request.path:
		lang = "tr/"

	inpt = request.form['username']
	inpt2 = request.form['password']
	log("login posted. Username: {} , password: {}".format(inpt, inpt2))

	if user_exists(inpt) and get_password_for(inpt) == inpt2:
		log("login success")
		return render_template('{}/{}login_success.html'.format(user, lang))
	
	else:
		log("login failed. Wrong username or password")
		attempt = attempt + 1
		if attempt > 2:
			return render_template('{}/{}login_exit.html'.format(user, lang))

	error = "Wrong username or password"
	if "/tr/" in request.path:
		error = "Hatalı kullanıcı adı veya parola"

	return render_template('{}/{}login.html'.format(user, lang), error=error)



# Successful login page
@app.route('/1/login_success', methods=['GET'])
@app.route('/2/login_success', methods=['GET'])
@app.route('/3/login_success', methods=['GET'])
@app.route('/4/login_success', methods=['GET'])
@app.route('/5/login_success', methods=['GET'])
@app.route('/6/login_success', methods=['GET'])
@app.route('/1/tr/login_success', methods=['GET'])
@app.route('/2/tr/login_success', methods=['GET'])
@app.route('/3/tr/login_success', methods=['GET'])
@app.route('/4/tr/login_success', methods=['GET'])
@app.route('/5/tr/login_success', methods=['GET'])
@app.route('/6/tr/login_success', methods=['GET'])
def login_success_page():
	user = request.path.split("/")[1]
	log("Successful login")
	if "/tr/" in request.path:
		return render_template('{}/tr/login_success.html'.format(user))

	return render_template('{}/login_success.html'.format(user))





# Successful register page
@app.route('/1/register_success', methods=['GET'])
@app.route('/2/register_success', methods=['GET'])
@app.route('/3/register_success', methods=['GET'])
@app.route('/4/register_success', methods=['GET'])
@app.route('/5/register_success', methods=['GET'])
@app.route('/6/register_success', methods=['GET'])
@app.route('/1/tr/register_success', methods=['GET'])
@app.route('/2/tr/register_success', methods=['GET'])
@app.route('/3/tr/register_success', methods=['GET'])
@app.route('/4/tr/register_success', methods=['GET'])
@app.route('/5/tr/register_success', methods=['GET'])
@app.route('/6/tr/register_success', methods=['GET'])
def register_success_page():
	user = request.path.split("/")[1]
	log("Successful register")
	if "/tr/" in request.path:
		return render_template('{}/tr/register_success.html'.format(user))	

	return render_template('{}/register_success.html'.format(user))








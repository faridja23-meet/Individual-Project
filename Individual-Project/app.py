from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

#Code goes below here

cartItems = []
cartTotal = 0



firebaseConfig = {
  "apiKey": "AIzaSyDePOkf29fcM7ITGzqd3QRSbUS5G935cz8",
  "authDomain": "farid-proj.firebaseapp.com",
  "projectId": "farid-proj",
  "storageBucket": "farid-proj.appspot.com",
  "messagingSenderId": "794880827466",
  "appId": "1:794880827466:web:33243626a16990f2f546b3",
  "measurementId": "G-4B69T0S2R9",
  "databaseURL" :"https://farid-proj-default-rtdb.europe-west1.firebasedatabase.app/"

}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()

#watches = [['Smart Watch Gen A', '$40.00 - $80.00'], ['Bands','$18.00'], ['Gen_B', '$25.00'], ['Gen_C', '$40.00']]
#for watch in watches:
	#db.child("Watches").push(watch)


@app.route('/', methods=['GET', 'POST'])
def signin():
	 error = ""
	 if request.method == 'POST':
	 	email = request.form['email']
	 	password = request.form['password']
	 	try:
	 		login_session['user'] = auth.sign_in_with_email_and_password(email, password)
	 		return render_template("login.html")
	 	except:
	 		error = "Authentication failed"
	 return render_template("login.html")


# @app.route('/addItem/<string:code>')
# def addItem(code):
# 	watch = db.child("Watches").child(code).get().val()
# 	bought_watches.append(code)

# 	return redirect(url_for('index'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
	error = ""
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		full_name = request.form['full_name']
		username = request.form ['username']

		try:
			login_session['user'] = auth.create_user_with_email_and_password(email, password)
			user1 = {"email":email, "password": password, "full_name": full_name, "username":username  }
			db.child("Users").child(login_session["user"]["localId"]).set(user1)
			return redirect(url_for('index'))
		except:
			error = "Authentication failed"
	return render_template("signup.html")

@app.route('/index', methods=['GET', 'POST'])
def index():
	return render_template("index.html", username = db.child("Users").child(login_session['user']['localId']).child("username").get().val())

@app.route('/aboutus', methods=['GET', 'POST'])
def aboutus():
	 
	return render_template("aboutus.html")




#Code goes above here

if __name__ == '__main__':
    app.run(debug=True)
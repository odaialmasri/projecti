from flask import Flask,request,render_template, redirect
import dataset


app = Flask(__name__)


db=dataset.connect("sqlite:///projecti")

accounts=db["accounts"]
projects=db["projects"]

Login = False


@app.route("/")
def home():
	return render_template("index.html")


@app.route("/signup",methods=["post","get"])
def signup():
	global Login
	if(request.method=="POST"):
		name=request.form["name"]
		email=request.form["email"]
		password=request.form["password"]
		pconfirm=request.form["password-confirm"]
		echeck=accounts.find(email=email)
		echeck2=len(list(echeck))
		if password==pconfirm and echeck2==0:
			accounts.insert(dict(name=name,email=email,password=password))
			return redirect('/login')
		else:
			return redirect('/signup')
	else:
		return render_template("signup.html", login=Login)



@app.route("/login",methods=["post","get"])
def login():
	global Login

	if(request.method=="POST"):
		email=request.form["email"]
		password=request.form["password"]
		e=accounts.find(email=email,password=password)
		check=len(list(e))
		if check != 0:
			Login= True
			return redirect ('/view') 

		else:
			Login= False
			return render_template("login.html", login=Login)
	else:
		Login= False
		return render_template("login.html", login=Login)


@app.route("/out",methods=["post","get"])
def signout():
	global Login
	global Ema
	Login=False
	Ema=""
	return redirect('/')


@app.route("/view")
def projects():
	return render_template("projects.html")

@app.route("/view-projects-info")
def info():
	return render_template("projects-info.html")
	if(request.method == "POST"):
		name = request.form["name"]
		factory = request.form["factory"]
		company = request.form["company"]
		Describtion= request.form["Describtion"]
		projects.insert(dict(name=name , factory= factory , company=company , Describtion=Describtion))
		return render_template("projects.html", projects=projects)
	else:
		return render_template("projects-info.html")

	



if __name__ == "__main__":

	app.run()



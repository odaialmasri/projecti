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


@app.route("/signup/<typ>",methods=["post","get"])
def signup(typ):
	global Login
	if(request.method=="POST"):
		name=request.form["name"]
		email=request.form["email"]
		password=request.form["password"]
		pconfirm=request.form["password-confirm"]
		echeck=accounts.find(email=email)
		echeck2=len(list(echeck))
		if password==pconfirm and echeck2==0:
			print typ
			accounts.insert(dict(name=name,email=email,password=password,ty=typ))
			return redirect('/login')
		else:
			return redirect('/signup'+typ)
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
		cc=e['ty']
		if check != 0:
			if cc == "sponser":
				Login= True
				return redirect ('ss')
			elif cc == "client":
				Login= True
				return redirect ('hh')
			Login= True
			return redirect ('/view') 
		else:
			Login= False
			return render_template("login.html",login=Login)
	else:
		Login= False
		return render_template("login.html",login=Login)


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
		Nameofidea = request.form["Nameofidea"]
		Email = request.form["Email"]
		Describtion= request.form["Describtion"]
		projects.insert(dict(name=name , Nameofidea= Nameofidea , Email=Email , Describtion=Describtion))
		return render_template("projects.html", projects=projects)
	else:
		return render_template("projects-info.html")

	



if __name__ == "__main__":
	app.run(port=5000)


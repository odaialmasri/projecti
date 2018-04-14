from flask import Flask,request,render_template, redirect
import dataset

app = Flask(__name__)

db=dataset.connect("sqlite:///projecti")

account=db["account"]
projects=db["projects"]

Login = False

@app.route("/")
def home():
	return render_template("index.html")


@app.route("/signup/<path:type>",methods=["post","get"])
def signup(type):
	print(type , request.method , "request.method")
	global Login
	if(request.method=="POST"):
		#print type , "signup type"
		name=request.form["name"]
		email=request.form["email"]
		password=request.form["password"]
		pconfirm=request.form["password-confirm"]
		echeck=account.find(email=email)
		echeck2=len(list(echeck))
		if password==pconfirm and echeck2==0:
			account.insert(dict(name=name,email=email,password=password,type=type))
			return redirect('/login')
		else:
			return redirect('/signup/'+type)
	else:
		return render_template("signup.html", login=Login, type=type)



@app.route("/login",methods=["post","get"])
def login():
	global Login
	print request.method

	if(request.method=="POST"):
		email=request.form["email"]
		password=request.form["password"]
		e=account.find_one(email=email,password=password)
		check=len(list(e))
		#for x in e:
			#print x
		
		#print check , list(e) ,e['type'] 
		if check != 0:
			c=e['type']
			print c
			if c == "sponsor":
				Login= True
				return redirect ('/ss')
			elif c == "client":
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
	app.run(port=5002)


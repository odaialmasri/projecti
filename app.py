from flask import Flask,request,render_template, redirect
import dataset

app = Flask(__name__)

db=dataset.connect("sqlite:///projecti")

account=db["account"]
project=db["project"]


Login = False

@app.route("/")
def home():
	global Login
	return render_template("index.html",login=Login)

@app.route("/signup/<path:type>",methods=["post","get"])
def signup(type):
	global Login
	if(request.method=="POST"):
		name=request.form["name"]
		email=request.form["email"]
		password=request.form["password"]
		pconfirm=request.form["password-confirm"]
		echeck=account.find(email=email)
		echeck2=len(list(echeck))
		if password==pconfirm and echeck2==0:
			account.insert(dict(name=name,email=email,password=password,type=type))
			if type == "sponsor":
				Login= True
				return redirect ('/view')
			elif type == "client":
				Login= True
				return redirect ('/enterproject')
		else:
			#return redirect('/signup/'+type)
			return render_template("signup.html",type=type,emailCheck=echeck2,pass1=password,pass2=pconfirm)
	else:
		return render_template("signup.html", login=Login, type=type)



@app.route("/login",methods=["post","get"])
def login():
	global Login
	
	if(request.method=="POST"):
		email=request.form["email"]
		password=request.form["password"]
		e=account.find_one(email=email,password=password)
		if e!= None:
			c=e['type']
			if c == "sponsor":
				Login= True
				return redirect ('/view')
			elif c == "client":
				Login= True
				return redirect ('/enterproject') 
		else:
			Login= False
			return render_template("login.html",login=Login,type=type,check=e)
	else:
		Login= False
		return render_template("login.html",login=Login,type=type)


@app.route("/logout",methods=["post","get"])
def signout():
	global Login
	Login=False
	return render_template('index.html',login=Login)



@app.route("/enterproject",methods=["post","get"])
def info():
	global Login
	if(request.method == "POST"):
		name=request.form["name"]
		ideaName=request.form["ideaName"]
		email=request.form["email"]
		describtion=request.form["describtion"]
		projectPhoto=request.form["projectPhoto"]
		project.insert(dict(name=name,ideaName=ideaName,email=email,describtion=describtion,projectPhoto=projectPhoto))
		return render_template("projects.html",login=Login,type=type,project=db["project"])
	else:
		return render_template("enterproject.html",login=Login,type=type)



@app.route("/view")
def projects():
	global Login
	return render_template ("projects.html",project=db["project"],login=Login)



@app.route("/moreinfo/<id>")
def moreinfo(id):
	global Login
	mi=project.find_one(ideaName=id)
	return render_template("projects-details.html",project=mi,login=Login)



if __name__ == "__main__":


	app.run(port=5003)



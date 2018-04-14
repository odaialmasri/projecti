from flask import Flask,request,render_template, redirect
import dataset

app = Flask(__name__)

db=dataset.connect("sqlite:///projecti")

account=db["account"]
project=db["project"]

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
				return redirect ('/view')
			elif c == "client":
				Login= True
				return redirect ('/enterproject') 
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



@app.route("/enterproject",methods=["post","get"])
def info():
	if(request.method == "POST"):
		name=request.form["name"]
		ideaName=request.form["ideaName"]
		email=request.form["email"]
		describtion=request.form["describtion"]
		print (dict(name=name,ideaName=ideaName,email=email,describtion=describtion))
		project.insert(dict(name=name,ideaName=ideaName,email=email,describtion=describtion))
		return redirect("/view")
	else:
		return render_template("enterproject.html")




	

@app.route("/view")
def projects():
	return render_template ("projects.html",project=db["project"])



@app.route("/moreinfo")
def moreinfo():
	return render_template("projects-details.html",project=db["project"])

	



if __name__ == "__main__":
	app.run(port=5002)


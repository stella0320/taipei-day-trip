import sys
sys.path.append('/usr/local/lib/python3.10/dist-packages')

from flask import Flask, jsonify
from flask import render_template
from flask import request
from taipeiAttraction import TaipeiAttraction
import time

app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True

password = "root"

@app.route("/login")
def login():
	return render_template("login.html", time=str(time.time()))

# Pages
@app.route("/")
def index():
	return render_template("index.html", time=str(time.time()))

@app.route("/attraction/<id>", methods = ['GET'])
def attraction(id):
	return render_template("attraction.html", time=str(time.time()), id = id)

@app.route("/booking")
def booking():
	return render_template("booking.html")

@app.route("/test")
def test():
	return render_template("test.html")

@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")

@app.route("/api/mrts", methods = ['GET'])
def mrts():
	try:
		db_connect = TaipeiAttraction('localhost', 'root', password)
		result = db_connect.findAllMrt()
	except Exception as e:
		return jsonify(error=True, message="請按照情境提供對應的錯誤訊息"), 500
	return result

@app.route("/api/attraction/<attractionId>", methods = ['GET'])
def attractionApiById(attractionId):
	
	try:
		db_connect = TaipeiAttraction('localhost', 'root', password)
		result = db_connect.queryAttractionId(attractionId)
		if not result:
			return jsonify(error=True, message="請按照情境提供對應的錯誤訊息"), 400
	except Exception as e:
		return jsonify(error=True, message="請按照情境提供對應的錯誤訊息"), 500
	
	return result

@app.route("/api/attractions", methods = ['GET'])
def attractionsApi():
	try:
		page = int(request.args.get('page', '0'))
		keyword = request.args.get('keyword', '')
		db_connect = TaipeiAttraction('localhost', 'root', password)
		result = db_connect.queryAttractionApi(page, keyword)
	except Exception as e:
		return jsonify(error=True, message="請按照情境提供對應的錯誤訊息"), 500
	return result

@app.route("/api/user", methods = ['POST'])
def registrateNewUser():
	try:
		data = request.get_json()
		name = data['name']
		mail = data['mail']
		userPassword = data['password']
		db_connect = TaipeiAttraction('localhost', 'root', password)
		user = db_connect.queryUserByEmail(mail);
		if not user:
			db_connect.insertNewUser(name, mail, userPassword)
		else:
			return jsonify(error=True, message="註冊失敗，重複的 Email 或其他原因"), 400
	except Exception as e:
		print('Exception:' + str(e))
	 	# return jsonify(error=True, message=str(e)), 500
		return jsonify(error=True, message=str(e)), 500
	return "註冊成功";

app.run(host='0.0.0.0', port='3000')

# app.run(port='3000')
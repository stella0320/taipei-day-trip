import sys
sys.path.append('/usr/local/lib/python3.10/dist-packages')

from flask import Flask, jsonify
from flask import render_template
from flask import request
from taipeiAttraction import TaipeiAttraction
import time
import jwt

app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True

password = "jessie0320"
jwt_algorithms = "HS256"
jwt_key = "secrect_key"

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
		
		if not name:
			return jsonify(error=True, message="註冊失敗，需要填寫姓名"), 400
		elif (len(name) > 50):
			return  jsonify(error=True, message="註冊失敗，姓名長度不能超過50個字"), 400
		
		if not mail:
			return jsonify(error=True, message="註冊失敗，需要填寫信箱"), 400
		elif (len(mail) > 50):
			return jsonify(error=True, message="註冊失敗，信箱長度不能超過50個字"), 400
		
		if not userPassword:
			return jsonify(error=True, message="註冊失敗，需要填寫密碼"), 400
		elif (len(userPassword) > 30):
			return jsonify(error=True, message="註冊失敗，密碼長度不能超過30個字"), 400
		
		db_connect = TaipeiAttraction('localhost', 'root', password)
		user = db_connect.queryUserByEmail(mail)
		if not user:
			db_connect.insertNewUser(name, mail, userPassword)
			# user = db_connect.queryUserByEmail(mail)
		else:
			return jsonify(error=True, message="註冊失敗，Email已經註冊帳戶"), 400
	except Exception as e:
		print('Exception:' + str(e))
		return jsonify(error=True, message=str(e)), 500
	return "註冊成功，請登入系統";


@app.route('/api/user/auth', methods = ['PUT'])
def userAuth():
	form = request.get_json()
	mail = form['mail']
	password = form['password']

	if not mail:
		return jsonify(error=True, message="登入失敗，需要填寫信箱"), 400
	
	if not password:
		return jsonify(error=True, message="登入失敗，需要填寫密碼"), 400


	db_connect = TaipeiAttraction('localhost', 'root', password)
	user = db_connect.queryUserByEmailAndPassword(mail, password)

	if not user:
		return jsonify(error=True, message="登入失敗，信箱或密碼錯誤"), 400
	
	# 產生新的token
	data = {
		"email": user['user_email'],
  		"password": user['user_password']
	}

	# jwt_algorithms
	try:
		encoded = jwt.encode(data, jwt_key, algorithm=jwt_algorithms)
		return {"token" : encoded}
	except Exception as e:
		return jsonify(error=True, message=str(e)), 500
	

@app.route('/api/user/auth', methods = ['GET'])
def userAuthWithToken():
	try:
		authorization_token = request.headers.get('Authorization')
		token = None
		if authorization_token:
			authorization_token_parts = authorization_token.split(' ')
			if len(authorization_token_parts) == 2 and authorization_token_parts[0] == 'Bearer':
				token = authorization_token_parts[1]
		dataByToken = None
		if token:
			dataByToken = jwt.decode(token, jwt_key, algorithms=jwt_algorithms)

		user = None
		if dataByToken and dataByToken['email']:
			db_connect = TaipeiAttraction('localhost', 'root', password)
			user = db_connect.queryUserByEmail(dataByToken['email'])
		
		if user:
			return {
				'data' : {
				'id' : user['user_id'],
				'name': user['user_name'],
				'email' : user['user_email']
				}
			}
		return None
	except Exception as e:
		print(e)
		return jsonify(error=True, message=str(e)), 500

app.run(host='0.0.0.0', port='3000')

# app.run(port='3000')
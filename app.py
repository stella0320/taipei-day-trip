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

# Pages
@app.route("/")
def index():
	return render_template("index.html", time=str(time.time()))

@app.route("/attraction/<id>", methods = ['GET'])
def attraction(id):	
	print('id' + id);
	return render_template("attraction.html", time=str(time.time()))

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
		db_connect = TaipeiAttraction('localhost', 'root', 'jessie0320')
		result = db_connect.findAllMrt()
	except Exception as e:
		return jsonify(error=True, message="請按照情境提供對應的錯誤訊息"), 500
	return result

@app.route("/api/attraction/<attractionId>", methods = ['GET'])
def attractionApiById(attractionId):
	
	try:
		db_connect = TaipeiAttraction('localhost', 'root', 'jessie0320')
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
		db_connect = TaipeiAttraction('localhost', 'root', 'jessie0320')
		result = db_connect.queryAttractionApi(page, keyword)
	except Exception as e:
		return jsonify(error=True, message="請按照情境提供對應的錯誤訊息"), 500
	return result

app.run(host='0.0.0.0', port='3000')

# app.run(port='3000')
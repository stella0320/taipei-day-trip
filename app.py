import sys
sys.path.append('/usr/local/lib/python3.10/dist-packages')

from flask import Flask
from flask import render_template
from taipeiAttraction import TaipeiAttraction

app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True

# Pages
@app.route("/")
def index():
	return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")
@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")

@app.route("/api/mrts", methods = ['GET'])
def mrts():
	db_connect = TaipeiAttraction('localhost', 'root', 'root')
	result = db_connect.findAllMrt()
	return result

@app.route("/api/attraction/<attractionId>", methods = ['GET'])
def attractionApi(attractionId):
	db_connect = TaipeiAttraction('localhost', 'root', 'root')
	result = db_connect.queryAttractionId(attractionId)
	return result

app.run(host='34.214.175.62', port='3000')
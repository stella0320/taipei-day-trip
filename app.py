import sys
sys.path.append('/usr/local/lib/python3.10/dist-packages')

from flask import Flask, jsonify
from flask import render_template
from flask import request
from taipeiAttraction import TaipeiAttraction
from tapPay import TapPay
import time
from datetime import datetime
import jwt
import logging
import traceback
today = datetime.now().strftime("%Y-%m-%d")


logging.basicConfig(filename='./log/record-'+ today + '.log', level=logging.DEBUG, encoding='utf-8', format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

# for console setting
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)

# 設定輸出格式
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# handler 設定輸出格式
console.setFormatter(formatter)
# 加入 hander 到 root logger
logging.getLogger('').addHandler(console)


app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True

password = "jessie0320"
jwt_algorithms = "HS256"
jwt_key = "secrect_key"

tap_pay_url = 'https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime'
tap_pay_partner_key = 'partner_yvNAtvcEOFaJG9IimrMvG5FxsPFBbtmBKxta3SNRnm2yxgaTWJ0USEMG'
tap_pay_merchant_id = 'jessie0320_NCCC'
# db_connect = TaipeiAttraction('localhost', 'root', password)
		
# Pages
@app.route("/")
def index():
	return render_template("index.html", time=str(time.time()))

@app.route("/attraction/<id>", methods = ['GET'])
def attraction(id):

	return render_template("attraction.html", time=str(time.time()), id = id)

@app.route("/booking")
def booking():
	return render_template("booking.html", time=str(time.time()))
@app.route("/test")
def test():
	return render_template("test.html")

@app.route("/thankyou")
def thankyou():
	orderNumber = request.args.get("number", "")
	orderId = int(orderNumber[-3:])

	if not orderId:
		return render_template("index.html", time=str(time.time()))
	
	db_connect = TaipeiAttraction('localhost', 'root', password)
	# queryOrderByUserIdAndOrderId
	orders = db_connect.queryOrderByOrderId(orderId)
	tappayResponseStatus = 200
	if orders and len(orders) > 0:
		tappayResponseStatus = orders[0]['tappay_response_status']
	return render_template("thankyou.html", time=str(time.time()), orderNumber = orderNumber, tappayResponseStatus = tappayResponseStatus)

@app.route("/api/mrts", methods = ['GET'])
def mrts():
	try:
		db_connect = TaipeiAttraction('localhost', 'root', password)
		result = db_connect.findAllMrt()
	except Exception as e:
		app.logger.debug(str(e), exc_info=True)
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
		app.logger.error(str(e), exc_info=True)
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
		app.logger.error(str(e), exc_info=True)
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
		else:
			return jsonify(error=True, message="註冊失敗，Email已經註冊帳戶"), 400
	except Exception as e:
		app.logger.error(str(e), exc_info=True)
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
		app.logger.error(str(e), exc_info=True)
		return jsonify(error=True, message=str(e)), 500
	

@app.route('/api/user/auth', methods = ['GET'])
def userAuthWithToken():
	try:
		authorization_token = request.headers.get('Authorization')
		token = None
		if authorization_token:
			authorization_token_parts = authorization_token.split(' ')
			if len(authorization_token_parts) == 2 and authorization_token_parts[0] == 'Bearer':
				token = authorization_token_parts[1].strip()
		dataByToken = None
		if token:
			dataByToken = jwt.decode(token, jwt_key, algorithms=jwt_algorithms)

		user = None
		if dataByToken and dataByToken['email']:
			db_connect = TaipeiAttraction('localhost', 'root', password)
			user = db_connect.queryUserByEmail(dataByToken['email'])
			app.logger.info('Login User Name:%s', user['user_name'])
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
		app.logger.error(str(e), exc_info=True)
		return jsonify(error=True, message=str(e)), 500


@app.route('/api/booking', methods = ['GET'])
def queryBookingList():
	userAuth = userAuthWithToken()
	user = None
	if userAuth:
		user = userAuth['data']
	
	if not user:
		return jsonify(error=True, message='未登入系統，拒絕存取'), 403
	
	db_connect = TaipeiAttraction('localhost', 'root', password)
	tripList = db_connect.findBookingTripByUserId(user['id'])

	tripWithAttrationList = []
	if tripList:
		for trip in tripList:
			attrationId = trip['attraction_id']
		
			db_connect = TaipeiAttraction('localhost', 'root', password)
			attractionInfo = db_connect.queryAttractionId(attrationId)
			if attractionInfo:
				attractionInfo = attractionInfo['data']
		

			tripWithAttration = {
				"tripId": trip['trip_id'],
				"attraction":attractionInfo,
				"date": trip['trip_date'],
				"time": trip['trip_period'],
				"price": trip['trip_fee'],
				"orderId":trip['order_id']
			}

			tripWithAttrationList.append(tripWithAttration)
	
	return {"data": tripWithAttrationList}

@app.route('/api/booking', methods = ['POST'])
def bookingNewTrip():
	try:
		userAuth = userAuthWithToken()

		if not userAuth:
			return jsonify(error=True, message='未登入系統，拒絕存取'), 403

		user = userAuth['data']
		form = request.get_json()
		attractionId = form['id']
		tripDate = form['tripDate']
		tripPeriod = form['tripPeriod']
		if not attractionId or not tripDate or not tripPeriod:
			return jsonify(error=True, message='建立失敗，輸入不正確或其他原因'), 400

		db_connect = TaipeiAttraction('localhost', 'root', password)
		db_connect.inserNewBookingTrip(attractionId, user['id'], tripDate, tripPeriod)

	except Exception as e:
		app.logger.error(str(e), exc_info=True)
		return jsonify(error=True, message=str(e)), 500
	
	return jsonify(ok=True), 200

@app.route('/api/booking/<tripId>', methods = ['DELETE'])
def deleteTrip(tripId):
	
	userAuth = userAuthWithToken()

	if not userAuth:
		return jsonify(error=True, message='未登入系統，拒絕存取'), 403

	
	if tripId:
		db_connect = TaipeiAttraction('localhost', 'root', password)
		# 要驗證delete的景點屬不屬於這個登入者
		db_connect.deleteBookingTripByTripId(tripId);
		return jsonify(ok=True), 200


@app.route('/api/orders', methods = ['POST'])
def createNewOrders():
	userAuth = userAuthWithToken()

	if not userAuth:
		return jsonify(error=True, message='未登入系統，拒絕存取'), 403
	
	try:
		user = userAuth['data']
		userId = user['id']
		form = request.get_json()
		prime = form['prime']
		order = form['order']
		orderId = form['orderId']
		tripList = order['trip']
		totalPrice = order['totalPrice']
		contact = order['contact']
		contactName = contact['name']
		contactEmail = contact['email']
		contactPhone = contact['phone']

		tripIdList = [int(trip['attraction']['id']) for trip in tripList]

		# 先檢查所有訂單是不是登入者的
		checkBookingTripResult = checkBookingTripByTripIdAndUserId(tripIdList, user['id'])

		if not checkBookingTripResult:
			return jsonify(error=True, message='訂單建立失敗，輸入不正確或其他原因'), 400
		
		db_connect = TaipeiAttraction('localhost', 'root', password)

		# 先查舊資料
		tempOrder = db_connect.queryTempOrderByUserId(userId)
		if not tempOrder:
			# 暫存 order
			db_connect2 = TaipeiAttraction('localhost', 'root', password)
			db_connect2.insertNewOrder(prime, userId, totalPrice, contactName, contactEmail, contactPhone)
			tempOrder = db_connect.queryTempOrderByUserId(userId)
		
		orderId = None
		createDate = datetime.now()
		if tempOrder and len(tempOrder) > 0:
			orderId = tempOrder[0]['order_id']
			createDate = tempOrder[0]['create_date']

		# 更新booking_trip
		updateOrderIdForBookingTrip(tempOrder, tripIdList, prime)
		
		# call tappay server
		tap_pay = TapPay(url = tap_pay_url, partner_key = tap_pay_partner_key, merchant_id = tap_pay_merchant_id, logger = app.logger)
		
		
		tap_pay_request_data = {
			"prime": prime,
			"details":"Order id:" + str(orderId),
			"amount": totalPrice,
			"cardholder": {
				"phone_number": contactPhone,
				"name": contactName,
				"email": contactEmail
			}
		}
		tap_pay_response = tap_pay.make_request(data=tap_pay_request_data)
		tap_pay_response_status = tap_pay_response.status

		
		tap_pay_response_data = tap_pay.getJsonResponse()
		orderNumber = None
		if createDate:
			createDateStr = createDate.strftime("%Y%m%d")
			orderNumber = createDateStr + str(orderId).zfill(3)
		
		tap_pay_response_data['order_number'] = orderNumber
		db_connect.updateOrdersForTapPayInfo(tapPayResponseStatus = tap_pay_response_status, tapPayResponseData = tap_pay_response_data, orderId = orderId)
		
		if tap_pay_response_status == 200:
			db_connect3 = TaipeiAttraction('localhost', 'root', password)
			db_connect3.updateStatusForBookingTrip(orderId = orderId, statusCode = 1)
			# 更新刷卡狀態
		else:
			return jsonify(error=True, message="訂單建立失敗，輸入不正確或其他原因"), 400
		
		app.logger.info("tap_pay_response:%s", tap_pay_response_data)
		# return tempOrder
		# orderId
		
		return {"data": {
			"number": orderNumber,
			"payment" : {
				"status":tap_pay_response_data['status'],
				"message":tap_pay_response_data['msg']
			}
		}}
	except Exception as e:
		app.logger.error(str(e), exc_info=True)
		return jsonify(error=True, message=str(e)), 500

def updateOrderIdForBookingTrip(tempOrder, tripIdList, prime):
	orderId = None
	if tempOrder:
		orderId = tempOrder[0]['order_id']
		
	if orderId:
		orderId = int(orderId)
		db_connect = TaipeiAttraction('localhost', 'root', password)
		db_connect.updateOrderIdForBookingTrip(orderId, tripIdList)

		db_connect2 = TaipeiAttraction('localhost', 'root', password)
		db_connect2.updatePrimeByOrderId(prime, orderId)

def checkBookingTripByTripIdAndUserId(tripIdList, userId):
	check = True
	for tripId in tripIdList:
		if tripId:
			db_connect = TaipeiAttraction('localhost', 'root', password)
			tempTripRecord = db_connect.findBookingTripByTripIdAndUserId(tripId, userId)
			if not tempTripRecord:
				check = False
		else:
			check = False

		if not check:
			break

	return check
app.run(host='0.0.0.0', port='3000')

# app.run(port='3000')
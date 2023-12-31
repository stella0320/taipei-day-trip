import mysql.connector


class TaipeiAttraction(object):
    def __init__(self, host, user, password):
        self.__host = host
        self.__user = user
        self.__password = password

    def __open__(self):
        try:
            self.__connect = mysql.connector.connect(host = self.__host, user= self.__user, password= self.__password, pool_name = 'mypool', pool_size = 30)
            self.__cursor = self.__connect.cursor()
        except mysql.connector.Error as e:
            # Todo 測試
            print("Error %s" % (e))
                

    def __close__(self):
        self.__connect.close()


    def __commit__(self):
        self.__connect.commit()

    def insertNewUser(self, userName, email, password):
        insertSql = "Insert into taipei_attraction.users (user_name, user_email, user_password) values (%s, %s, %s)"
        self.__open__()
        self.__cursor.execute(insertSql, (userName, email, password, ))
        self.__commit__()
        self.__close__()

    def queryUserByEmail(self, email):
        sql = "select * from taipei_attraction.users"
        sql += " where user_email = %s"
        self.__open__()
        self.__cursor.execute(sql, (email, ))
        result = self.__cursor.fetchone()
        self.__close__()
        if result and len(result) > 0:
            return dict(zip(self.__cursor.column_names, result))
        
        return None
    
    def queryUserByEmailAndPassword(self, email, password):
        sql = "select * from taipei_attraction.users"
        sql += " where user_email = %s and user_password = %s"
        self.__open__()
        self.__cursor.execute(sql, (email, password, ))
        result = self.__cursor.fetchone()
        self.__close__()
        if result and len(result) > 0:
            return dict(zip(self.__cursor.column_names, result))
        
        return None

    def queryMrtByMrtName(self, mrtName):
        
        sql = "select * from taipei_attraction.mrt where mrt_name = %s"

        self.__open__()
        self.__cursor.execute(sql, (mrtName, ))
        
        result = self.__cursor.fetchone()
        self.__close__()
        if result and len(result) > 0:
            return dict(zip(self.__cursor.column_names, result))
        
        return None

    def insertNewMrt(self, mrtName):

        if not mrtName:
            mrtName = "NULL"

        insertSql = "Insert into taipei_attraction.mrt (mrt_name) values (%s)"
        self.__open__()
        self.__cursor.execute(insertSql, (mrtName, ))
        self.__connect.commit()
        self.__close__()

    
    def queryCategoryByCategoryName(self, categoryName):
        sql = "select * from taipei_attraction.attraction_category where category_name = %s"

        self.__open__()
        self.__cursor.execute(sql, (categoryName, ))
        
        result = self.__cursor.fetchone()
        self.__close__()
        if result and len(result) > 0:
            return dict(zip(self.__cursor.column_names, result))
        
        return None
    
    
    def insertNewCategory(self, categoryName):

        if not categoryName:
            return None

        insertSql = "Insert into taipei_attraction.attraction_category (category_name) values(%s)"
        self.__open__()
        self.__cursor.execute(insertSql, (categoryName, ))
        self.__connect.commit()
        self.__close__()



    def insertNewImage(self, attractionId, imageUrl):
        insertSql = "Insert into taipei_attraction.attraction_image (attraction_id, image_url) values(%s, %s)"
        self.__open__()
        self.__cursor.execute(insertSql, (attractionId, imageUrl, ))
        self.__connect.commit()
        self.__close__()

    def queryImageUrlListByAttractionId(self, attractionId):
        
        sql = "select * from taipei_attraction.attraction_image where attraction_id = %s"

        self.__open__()
        self.__cursor.execute(sql, (attractionId, ))
        
        result = self.__cursor.fetchall()
        self.__close__()
        if result and len(result) > 0:
            result = [dict(zip(self.__cursor.column_names, row)) for row in result]
            return [item['image_url'] for item in result]
        
        return None

    def insertNewAttraction(self, attractionName, categoryId, mrtId, attractionDescription, address, transport, lat, lng):
        insertSql = "Insert into taipei_attraction.attraction (attraction_name, category_id, mrt_id, description, address, transport, lat, lng) "
        insertSql += "values(%s, %s, %s, %s, %s, %s, %s, %s)"
        self.__open__()
        self.__cursor.execute(insertSql, (attractionName, categoryId, mrtId, attractionDescription, address, transport, lat, lng, ))
        self.__connect.commit()
        self.__close__()

    def queryAttractionByName(self, name):
        sql = "select * from taipei_attraction.attraction where attraction_name = %s"

        self.__open__()
        self.__cursor.execute(sql, (name, ))
        
        result = self.__cursor.fetchone()
        self.__close__()
        if result and len(result) > 0:
            return dict(zip(self.__cursor.column_names, result))
        
        return None

    def insertNewAttractionImage(self, attraction_id, url):
        sql = 'Insert into taipei_attraction.attraction_image (attraction_id, image_url) values (%s, %s)'
        self.__open__()
        self.__cursor.execute(sql, (attraction_id, url, ))
        self.__connect.commit()
        self.__close__()

    def findAllMrt(self):
        sql = "select a.mrt_name from taipei_attraction.mrt a "
        sql += "right join taipei_attraction.attraction b "
        sql += "on a.mrt_id = b.mrt_id "
        sql += "where a.mrt_name is not null "
        sql += "group by a.mrt_name "
        sql += "order by count(b.attraction_name) desc "
        self.__open__()
        self.__cursor.execute(sql)
        result = self.__cursor.fetchall()
        self.__close__()

        return {
            'data': [item[0] for item in result]
        }
    
    def queryAttractionId(self, attractionId):
        sql = "select * from taipei_attraction.attraction a, taipei_attraction.attraction_category b, taipei_attraction.mrt c "
        sql += "where a.attraction_id = %s and a.mrt_id = c.mrt_id and a.category_id = b.category_id "
        self.__open__()
        self.__cursor.execute(sql, (attractionId, ))
        result = self.__cursor.fetchone()
        self.__close__()
        if result and len(result) > 0:
            result = dict(zip(self.__cursor.column_names, result))
            attraction_id = result['attraction_id']
            imageList = self.queryImageUrlListByAttractionId(attraction_id)
            return {
                'data' :{
                    'id': result['attraction_id'],
                    'name': result['attraction_name'],
                    'category': result['category_name'],
                    'description': result['description'],
                    'address': result['address'],
                    'transport': result['transport'],
                    'mrt': result['mrt_name'],
                    'lat': result['lat'],
                    'lng': result['lng'],
                    'images': imageList
                }
            }
        
    def countAttractionApi(self, keyword):
        if not keyword:
            sql = 'select count(*) count from taipei_attraction.attraction'
        else:
            sql = 'select count(*) count from taipei_attraction.attraction a '
            sql += 'left join taipei_attraction.mrt b '
            sql += 'on a.mrt_id = b.mrt_id '
            sql += 'where a.attraction_name like %s or b.mrt_name = %s '

        self.__open__()

        if not keyword:
            self.__cursor.execute(sql)
        else:
            self.__cursor.execute(sql, ('%' + keyword + '%',keyword, ))
        result = self.__cursor.fetchone()
        self.__close__()

        return list(result)[0]
    
    def queryAttractionPageDataApi(self, page, keyword):
        sql = 'select c.*, d.* from ( '
        sql += 'select b.mrt_name, a.* from taipei_attraction.attraction a '
        sql += 'left join taipei_attraction.mrt b '
        sql += 'on a.mrt_id = b.mrt_id '
        sql += 'where a.attraction_name like %s or b.mrt_name = %s '
        sql += 'order by attraction_id '
        sql += 'LIMIT %s,%s) c '
        sql += 'left join taipei_attraction.attraction_category d '
        sql += 'on c.category_id = d.category_id '

        self.__open__()
        self.__cursor.execute(sql, ('%' + keyword + '%',keyword, page * 12, 12, ))

        result = self.__cursor.fetchall()
        self.__close__()

        dataList = []

        if result and len(result) > 0:
            results = [dict(zip(self.__cursor.column_names, row)) for row in result]
            for result in results:
                attraction_id = result['attraction_id']
                imageList = self.queryImageUrlListByAttractionId(attraction_id)
                data = {
                    'id': result['attraction_id'],
                    'name': result['attraction_name'],
                    'category': result['category_name'],
                    'description': result['description'],
                    'address': result['address'],
                    'transport': result['transport'],
                    'mrt': result['mrt_name'],
                    'lat': result['lat'],
                    'lng': result['lng'],
                    'image': imageList
                }
                dataList.append(data)
        
        return dataList

    def queryAttractionApi(self, page, keyword):
        # page必填 給exception
        totalCount = self.countAttractionApi(keyword)

        # page * 12 ~ (page + 1) * 12
        if totalCount > (page + 1) * 12:
            nextPage = page + 1
        else:
            nextPage = None

        data = self.queryAttractionPageDataApi(page, keyword)
        result = {
            "nextPage": nextPage,
            "data": data
        }

        return result
    
    def inserNewBookingTrip(self, attractionId, userId, tripDate, tripPeriod):

        tripFee = 2000
        if tripPeriod == 'afternoon':
            tripFee = 2500
        sql = 'Insert into taipei_attraction.booking_trip (trip_status, trip_date, attraction_id, user_id, trip_period, trip_fee) values (%s, %s, %s, %s, %s, %s)'
        self.__open__()
        self.__cursor.execute(sql, (0, tripDate, attractionId, userId, tripPeriod, tripFee, ))
        self.__connect.commit()
        self.__close__()


    def findBookingTripByUserId(self, userId):
        sql = "select * from taipei_attraction.booking_trip where user_id = %s and trip_status = 0"
        self.__open__()
        self.__cursor.execute(sql, (userId, ))        
        result = self.__cursor.fetchall()
        self.__close__()
        if result and len(result) > 0:
            return [dict(zip(self.__cursor.column_names, row)) for row in result]
        
        return None
    
    def deleteBookingTripByTripId(self, tripId):
        sql = 'delete from taipei_attraction.booking_trip where trip_id = %s'
        self.__open__()
        self.__cursor.execute(sql, (tripId, ))
        self.__connect.commit()
        self.__close__()

    def findBookingTripByTripIdAndUserId(self, tripId, userId):
        sql = "select * from taipei_attraction.booking_trip where trip_id = %s and user_id = %s and trip_status = 0"
        self.__open__()
        self.__cursor.execute(sql, (int(tripId), userId, ))   
        result = self.__cursor.fetchall()
        self.__close__()
        if result and len(result) > 0:
            return [dict(zip(self.__cursor.column_names, row)) for row in result]
        
        return None
    
    def insertNewOrder(self, prime, userId, amount, contact_name, contact_email, contact_phone):
        sql = "INSERT INTO taipei_attraction.orders (prime, amount, contact_name, contact_email, contact_phone, create_id) values"
        sql += " (%s, %s, %s, %s, %s, %s)"
        self.__open__()
        self.__cursor.execute(sql, (prime, int(amount), contact_name, contact_email, contact_phone, userId, ))
        self.__connect.commit()
        print(self.__cursor.lastrowid)
        self.__close__()

    def queryTempOrderByUserId(self, userId):
        sql = "select * from taipei_attraction.orders where create_id = %s and order_status = 0"
        self.__open__()
        self.__cursor.execute(sql, (userId, ))    
        result = self.__cursor.fetchall()
        self.__close__()
        if result and len(result) > 0:
            return [dict(zip(self.__cursor.column_names, row)) for row in result]
        
        return None
    
    def updateOrderIdForBookingTrip(self, orderId, bookingTripIdList):
        
        format_strings = ','.join(['%s'] * len(bookingTripIdList))
        sql = "update taipei_attraction.booking_trip "
        sql += " set order_id = %%s"
        sql += " where trip_id in (%s)" 
        orderId_tuple = (orderId, )
        sql = sql % format_strings
        self.__open__()
        self.__cursor.execute(sql, orderId_tuple + tuple(bookingTripIdList))
        self.__connect.commit()
        self.__close__()

    def updatePrimeByOrderId(self, prime, orderId):
        sql = "update taipei_attraction.orders "
        sql += " set prime = %s"
        sql += " where order_id = %s"

        self.__open__()
        self.__cursor.execute(sql, (prime, int(orderId), ))
        self.__connect.commit()
        self.__close__()

    def updateOrdersForTapPayInfo(self, tapPayResponseStatus, tapPayResponseData, orderId):
        
        responseStatus = tapPayResponseData['status']
        orderNumber = tapPayResponseData['order_number']
        sql = None
        params = None
        if tapPayResponseStatus != 200 or responseStatus != 0:
            sql = "update taipei_attraction.orders "
            sql += " set order_status=%s, tappay_response_status=%s, tappay_status_code=%s, order_number=%s"
            sql += " where order_id=%s"
            params = (0, tapPayResponseStatus, tapPayResponseData['status'], tapPayResponseData['order_number'], orderId, )
        else:
            sql = "update taipei_attraction.orders "
            sql += " set order_status=%s, tappay_response_status=%s, tappay_status_code=%s, order_number=%s, rec_trade_id=%s, bank_transaction_id=%s"
            sql += " where order_id=%s"
            params = (1, tapPayResponseStatus, tapPayResponseData['status'], tapPayResponseData['order_number'], tapPayResponseData['rec_trade_id'], tapPayResponseData['bank_transaction_id'], orderId, )
        self.__open__()
        self.__cursor.execute(sql, params)
        self.__connect.commit()
        self.__close__()


    def updateStatusForBookingTrip(self, orderId, statusCode):
        
        sql = "update taipei_attraction.booking_trip "
        sql += " set trip_status = %s"
        sql += " where order_id = %s" 
        self.__open__()
        self.__cursor.execute(sql, (statusCode, orderId, ))
        self.__connect.commit()
        self.__close__()

    def queryOrderByOrderId(self, orderId):
        sql = "select * from taipei_attraction.orders where order_id = %s"
        self.__open__()
        self.__cursor.execute(sql, (orderId, ))    
        result = self.__cursor.fetchall()
        self.__close__()
        if result and len(result) > 0:
            return [dict(zip(self.__cursor.column_names, row)) for row in result]
        
        return None

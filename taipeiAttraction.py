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
        except mysql.connector.errors as e:
            # Todo 測試
            for error_msg in e:
                print("Error %s" % (e))

    def __close__(self):
        self.__connect.close()

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

    def insertNewAttraction(self, attractionName, categoryId, mrtId, attractionDescription, address, transport, lat, lng):
        insertSql = "Insert into taipei_attraction.attraction (attraction_name, category_id, mrt_id, description, address, transport, lat, lng) "
        insertSql += "values(%s, %s, %s, %s, %s, %s, %s, %s)"
        self.__open__()
        self.__cursor.execute(insertSql, (attractionName, categoryId, mrtId, attractionDescription, address, transport, lat, lng, ))
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

        return [item[0] for item in result]
    
    def queryAttractionId(self, attractionId):
        sql = "select * from taipei_attraction.attraction a, taipei_attraction.attraction_category b, taipei_attraction.mrt c "
        sql += "where a.attraction_id = %s and a.mrt_id = c.mrt_id and a.category_id = b.category_id "
        self.__open__()
        self.__cursor.execute(sql, (attractionId, ))
        result = self.__cursor.fetchone()
        self.__close__()
        if result and len(result) > 0:
            result = dict(zip(self.__cursor.column_names, result))
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
                    'lng': result['lng']
                }
            }
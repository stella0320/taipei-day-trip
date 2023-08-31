from taipeiAttraction import TaipeiAttraction

db_connect = TaipeiAttraction('localhost', 'root', 'root')

allMrt = db_connect.findAllMrt()
attraction = db_connect.queryAttractionId(1)
print(attraction)
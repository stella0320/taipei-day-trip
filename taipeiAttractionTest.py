from taipeiAttraction import TaipeiAttraction

db_connect = TaipeiAttraction('localhost', 'root', 'root')

# allMrt = db_connect.findAllMrt()
# attraction = db_connect.queryAttractionId(1)
# print(attraction)

count = db_connect.countAttractionApi('北')
print(count)

data = db_connect.queryAttractionPageDataApi(1, '北')

print(data)

data1 = db_connect.queryAttractionApi(2, '北')

print(data1)
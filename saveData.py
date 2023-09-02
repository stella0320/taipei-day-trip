import json
from taipeiAttraction import TaipeiAttraction
import re

with open('data/taipei-attractions.json', encoding='utf-8') as file:
    dataSet = json.load(file)['result']['results']



db_connect = TaipeiAttraction('localhost', 'root', 'jessie0320')

for data in dataSet:
    
    category_name = data['CAT']
    name = data['name']
    mrt_name = data['MRT']
    attraction_description = data['description']
    address = data['address']
    transport = data['direction']
    lat = data['latitude']
    lng = data['longitude']
    files = data['file']

    #category

    category = db_connect.queryCategoryByCategoryName(category_name)
    if not category:
        db_connect.insertNewCategory(category_name)
        category = db_connect.queryCategoryByCategoryName(category_name)


    #mrt
    mrt = db_connect.queryMrtByMrtName(mrt_name)
    if not mrt:
        db_connect.insertNewMrt(mrt_name)
        mrt = db_connect.queryMrtByMrtName(mrt_name)

    if not category:
        category_id = None
    else:
        category_id = category['category_id']


    if not mrt:
        mrt_id = None
    else:
        mrt_id = mrt['mrt_id']

    attraction = db_connect.queryAttractionByName(name)

    if not attraction:
        db_connect.insertNewAttraction(name, category_id, mrt_id, attraction_description, address, transport, lat, lng)

    # 處理image url

    if files:
        # 使用正则表达式查找匹配的链接
        filesList = re.findall(r"[^https://www.travel.taipei][^.]+(?:\.jpg|\.JPG)", files)
        filesList = ['https://www.travel.taipei/' + file for file in filesList]

    if attraction and filesList:
        # insert image
        attraction_id = int(attraction['attraction_id'])
        for file_url in filesList:
            db_connect.insertNewImage(attraction_id, file_url)


        








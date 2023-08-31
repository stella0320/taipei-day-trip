import json
from taipeiAttraction import TaipeiAttraction

with open('data/taipei-attractions.json', encoding='utf-8') as file:
    dataSet = json.load(file)['result']['results']



db_connect = TaipeiAttraction('localhost', 'root', 'root')

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

    db_connect.insertNewAttraction(name, category_id, mrt_id, attraction_description, address, transport, lat, lng)



# txt = "https://www.travel.taipei/d_upload_ttn/sceneadmin/pic/11000848.jpghttps://www.travel.taipei/d_upload_ttn/sceneadmin/pic/11002891.jpghttps://www.travel.taipei/d_upload_ttn/sceneadmin/image/A0/B0/C0/D315/E70/F65/1e0951fb-069f-4b13-b5ca-2d09df1d3d90.JPGhttps://www.travel.taipei/d_upload_ttn/sceneadmin/image/A0/B0/C0/D260/E538/F274/e7d482ba-e3c0-40c3-87ef-3f2a1c93edfa.JPGhttps://www.travel.taipei/d_upload_ttn/sceneadmin/image/A0/B0/C0/D919/E767/F581/9ddde70e-55c2-4cf0-bd3d-7a8450582e55.JPGhttps://www.travel.taipei/d_upload_ttn/sceneadmin/image/A0/B0/C1/D28/E891/F188/77a58890-7711-4ca2-aebe-4aa379726575.JPG"

# print(len(txt))

# start = 0
# end = 5
# urlArray = []
# while (end + 26 < len(txt)):
#     position = txt.index("https://www.travel.taipei/", end)
#     position = min(len(txt), position)
#     urlArray.append(txt[start:position])
#     start = position
#     end = position + 1

# print(urlArray)

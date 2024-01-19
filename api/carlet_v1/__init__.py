import requests




def login(account='celine', password='8888good'):
    url = 'https://service.gama.carlet.com.tw/api/anonymous/admin/login'

    response = requests.post(url,json={
        'account':account,
        'password':password
    })

    if response.status_code == 200:
        print("登入成功")
        # print("回應內容:", response.json())
        token = response.headers.get('X-Auth-Token')
        return token
    else:
        print("登入失敗")
        print("錯誤碼:", response.status_code)
        print("錯誤內容:", response.text)
        raise Exception()




def get_product(token, product_id)->dict:
    url = f'https://service.gama.carlet.com.tw/api/admin/store/parts/{product_id}'
    response = requests.get(url, headers={'Authorization':f'Bearer {token}'})
    if response.status_code == 200:
        data = response.json()
        entity = data.get('entity')
        return entity
    else:
        print("索取失敗")
        print("錯誤碼:", response.status_code)
        print("錯誤內容:", response.text)
        raise Exception()



def check_product_exists(token, store, name):
    url = 'https://service.gama.carlet.com.tw/api/admin/store/partss'
    response = requests.get(url, params={'store':store, 'name':name}, headers={'Authorization':f'Bearer {token}'})
    if response.status_code == 200:
        data = response.json()
        entities = data.get('pager',{}).get('entities',[])
        if len(entities)==1:
            print(f"產品已存在 : {name}")
            return True, entities[0].get('id')
        elif not entities:
            return False, None
        else:
            raise Exception()

    else:
        print("查詢失敗")
        print("錯誤碼:", response.status_code)
        print("錯誤內容:", response.text)
        raise Exception()


def create_product(token, store, name, hours, price, cost, description='其他說明', purchase_notes='購買說明'):
    url='https://service.gama.carlet.com.tw/api/admin/store/parts'
    data = {
        "store": store,
        "name": name,
        "hour": hours,
        "price": price,
        "cost": cost,
        "is_enabled": 1,
        "enabled_at": "2000-01-01 00:00:00",
        "disabled_at": "2099-12-31 23:59:59",
        "description": description,
        "purchase_notes": purchase_notes,
    }
    response = requests.post(url, json=data, headers={'Authorization':f'Bearer {token}'})

    if response.status_code == 200:
        print(f'新增產品成功 : {name}')
        data = response.json()
        return True, data.get('entity',{})
    else:
        print("新增產品失敗")
        print("錯誤碼:", response.status_code)
        print("錯誤內容:", response.text)
        raise Exception()
    
def delete_product_image(token, product_id, image_uid):
    url=f'https://service.gama.carlet.com.tw/api/admin/store/parts/{product_id}/image/{image_uid}'
    response = requests.delete(url, headers={'Authorization':f'Bearer {token}'})
    if response.status_code == 200:
        print('刪除圖片成功')
    else:
        print("刪除圖片失敗")
        print("錯誤碼:", response.status_code)
        print("錯誤內容:", response.text)
        raise Exception()

def delete_all_product_image(token, product_entity:dict=None, product_id=None):
    if product_id:
        product_entity:dict = get_product(token, product_id)
    for photo in product_entity.get('photos',[]):
        delete_product_image(token, product_entity.get('id'), photo.get('uid'))

def add_product_image(token, product_id, image_path):
    url = f'https://service.gama.carlet.com.tw/api/admin/store/parts/{product_id}/image'

    with open(image_path, "rb") as file:
        response = requests.post(url, headers={'Authorization':f'Bearer {token}'}, files = {"file": file})
    if response.status_code == 200:
        print('新增圖片成功')
    else:
        print("新增圖片失敗")
        print("錯誤碼:", response.status_code)
        print("錯誤內容:", response.text)
        raise Exception()
    
# def add_product_image_if_not_exists(token, product_id, image_name):

#     product = get_product(token, product_id)
#     if not product.get('photos',[]):
#         add_product_image(token, product_id, image_name)
#     else:
#         print(f'商品{product_id}已存在照片')

def update_product_cateogry(token, product_id, category_id=210):
    url=f'https://service.gama.carlet.com.tw/api/admin/store/parts/{product_id}/categories'
    response = requests.put(url, json=[{
        'id':category_id,#輪胎
        'sid':999999,
    }], headers={'Authorization':f'Bearer {token}'})
    if response.status_code == 200:
        print('更新類別成功')
    else:
        print("更新類別失敗")
        print("錯誤碼:", response.status_code)
        print("錯誤內容:", response.text)
        raise Exception()

def _get_product_compatibility(token, product_id):

    url = f'https://service.gama.carlet.com.tw/api/admin/store/parts/{product_id}/match/vehicles'
    response = requests.get(url, headers={'Authorization':f'Bearer {token}'})

    all, sizes, makes, models_include, models_exclude = False, [], [], [], []
    if response.status_code == 200:
        data = response.json()
        entity = data.get('entity',{})

        all = entity.get('all')
        sizes = entity.get('size',[])
        makes = [ make.get('name') for make in entity.get('make')]
        models_include = [ vehicle.get('id') for vehicle in entity.get('model_include')]
        models_exclude = [ vehicle.get('id') for vehicle in entity.get('model_exclude')]
    else:
        print("取得產品相容車款失敗")
        print("錯誤碼:", response.status_code)
        print("錯誤內容:", response.text)
        raise Exception()
    
    return all, sizes, makes, models_include, models_exclude

def add_compatible_vehicle(token, product_id, vehicle_id):
    url = f'https://service.gama.carlet.com.tw/api/admin/store/parts/{product_id}/match/vehicles'

    all, sizes, makes, models_include, models_exclude = _get_product_compatibility(token, product_id)


    if vehicle_id in models_include:
        print("新增產品相容車款成功")
        return
    
    models_include.append(vehicle_id)

    response = requests.put(url, headers={'Authorization':f'Bearer {token}'},
                             json={
                                    "all": all,
                                    "size": sizes,
                                    "make": makes,
                                    "model_include": models_include,
                                    "model_exclude": models_exclude
                             })
    
    if response.status_code == 200:
        print("新增產品相容車款成功")
    else:
        print("新增產品相容車款失敗")
        print("錯誤碼:", response.status_code)
        print("錯誤內容:", response.text)
        raise Exception()



def add_compatible_vehicles(token, product_id, vehicle_ids):
    url = f'https://service.gama.carlet.com.tw/api/admin/store/parts/{product_id}/match/vehicles'
    all, sizes, makes, models_include, models_exclude = _get_product_compatibility(token, product_id)


    models_include += vehicle_ids
    response = requests.put(url, headers={'Authorization':f'Bearer {token}'},
                             json={
                                    "all": all,
                                    "size": sizes,
                                    "make": makes,
                                    "model_include": models_include,
                                    "model_exclude": models_exclude
                             })
    
    if response.status_code == 200:
        print("新增產品相容車款成功")
    else:
        print("新增產品相容車款失敗")
        print("錯誤碼:", response.status_code)
        print("錯誤內容:", response.text)
        raise Exception()








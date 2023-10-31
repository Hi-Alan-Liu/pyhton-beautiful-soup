# encoding:utf-8

from bs4 import BeautifulSoup
import pandas as pd
import json
import requests

# 需要解析的資料
html = '<div class="store space-y-7 sm__space-y-8"><div data-v-a5e48eb8="" class="store-info space-y-5 text-lg"><div data-v-a5e48eb8="" class="store-name space-x-5"><span data-v-a5e48eb8="" class="flex-shrink-0">店名</span><span data-v-a5e48eb8="" class="font-bold text-primary flex flex-col sm__flex-row sm__items-center">(高雄市)金玉堂：路竹店<!----><!----></span></div><div data-v-a5e48eb8="" class="address space-x-5"><span data-v-a5e48eb8="" class="flex-shrink-0">地址</span><address data-v-a5e48eb8="" class="not-italic flex justify-between items-center">高雄市路竹區國昌路16號<a data-v-a5e48eb8="" href="http://maps.google.com.tw/maps?q=高雄市路竹區國昌路16號" target="_blank" class="text-secondary flex-shrink-0">＞ 地圖</a></address></div><div data-v-a5e48eb8="" class="tel space-x-5"><span data-v-a5e48eb8="" class="flex-shrink-0">電話</span><span data-v-a5e48eb8="">07-6966802</span></div></div><div data-v-a5e48eb8="" class="store-info space-y-5 text-lg"><div data-v-a5e48eb8="" class="store-name space-x-5"><span data-v-a5e48eb8="" class="flex-shrink-0">店名</span><span data-v-a5e48eb8="" class="font-bold text-primary flex flex-col sm__flex-row sm__items-center">(高雄市)統一超商：路好<!----><!----></span></div><div data-v-a5e48eb8="" class="address space-x-5"><span data-v-a5e48eb8="" class="flex-shrink-0">地址</span><address data-v-a5e48eb8="" class="not-italic flex justify-between items-center">高雄市路竹區大社路162號<a data-v-a5e48eb8="" href="http://maps.google.com.tw/maps?q=高雄市路竹區大社路162號" target="_blank" class="text-secondary flex-shrink-0">＞ 地圖</a></address></div><div data-v-a5e48eb8="" class="tel space-x-5"><span data-v-a5e48eb8="" class="flex-shrink-0">電話</span><span data-v-a5e48eb8="">-</span></div></div></div>'

# 填入自己的 Google Maps API 金鑰
api_key = 'your_api_key_here'

soup = BeautifulSoup(html, 'html.parser')

# 列表
contact_list = []

# 將每個店整理成各筆資料
store_infos = soup.find_all('div', class_='store-info')

for store_info in store_infos:
    # 解析店名
    store_name = store_info.find('span', class_='font-bold').text.split('周邊商品販售中')[0]

    # 解析地址
    address = store_info.find('address').text.split('＞')[0]

    # 解析地圖連結
    map_link = store_info.find('a')['href']

    # 解析電話
    tel = store_info.find('div', class_='tel').text.split('電話')[1]

    # 建立 GOOGLE API URL
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}"

    # 發送請求
    response = requests.get(url)

    # 解析回傳的 JSON 資料
    data = json.loads(response.text)

    if data["status"] == "OK":
        
        # 取得經緯度
        lat = data["results"][0]["geometry"]["location"]["lat"]
        lng = data["results"][0]["geometry"]["location"]["lng"]


        # 建立字典
        contact_info = {
            'name': store_name,
            'address': address,
            'link': map_link,
            'tel': tel,
            'lat': lat,
            'lng': lng
        }

        # 把字典放進列表
        contact_list.append(contact_info)
    else:
        print("GOOGLE API ERROR")
        print(url)
        print(data)

print(contact_list)


# 建立 DataFrame
df = pd.DataFrame(contact_list)

# 將 DataFrame 寫入 Excel 檔案
with pd.ExcelWriter('contact_list.xlsx') as writer:
    df.to_excel(writer, index=False, sheet_name='Sheet1')

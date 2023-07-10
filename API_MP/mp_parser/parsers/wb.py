import requests


def parse_products(parse_data):
    products = [] 
    for page in range(1, 100):
        respons = requests.get(fr"https://search.wb.ru/exactmatch/ru/common/v4/search?TestGroup=main_page_reranker&TestID=186&appType=1&curr=rub&dest=-1257786&page={page}&query={parse_data}&regions=80,38,4,64,83,33,68,70,69,30,86,75,40,1,66,110,22,31,48,71,114&resultset=catalog&sort=popular&spp=0&suppressSpellcheck=false")
        if respons.text == '':
            break
        else:
            for j in respons.json()['data']['products']:
                products.append({'id': j['id'], 'brand': j['brand'], 'name': j['name'], 'price': f"{str(j['salePriceU'])[:-2]}.{str(j['salePriceU'])[-2:]}", 'link': f"https://www.wildberries.ru/catalog/{j['id']}/detail.aspx"})
    return products

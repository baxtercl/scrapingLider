from bs4 import BeautifulSoup
import requests
#import json
import csv 

URL_BASE ="https://www.lider.cl{}"
URL = URL_BASE.format("/supermercado/category/Frutas-y-Verduras/_/N-1vsgxxq?N=&No=0&Nrpp=80&isNavRequest=Yes")
FILECSV = "frutas-y-verduras.csv"
TOTAL=0

def grocery(url,np=1):

    global TOTAL
    req = requests.get(url)
    statusCode = req.status_code
    #data = {}
    #data['productos'] = []

    with open(FILECSV, 'w', newline='') as csvfile:
        datawriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        datawriter.writerow(['Name', 'Description', 'Price1', 'Price2', 'Image'])

    if statusCode == 200:
        html = BeautifulSoup(req.text, "html.parser")
        entradas = html.find('div', {"id": "content-prod-boxes"})

        for entrada in entradas.findAll("div",{"class":"box-product"}):
            image = entrada.find("img",{"class" : "img-responsive"})["src"]
            name = entrada.find("span",{"class" : "product-name"}).text
            desc = entrada.find("span",{"class" : "product-description"}).text
            price1 = entrada.find("span",{"class" : "price-sell"}).text
            price2 = entrada.find("span",{"class" : "product-round"}).text

            with open(FILECSV, 'a', newline='') as csvfile:
                datawriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                datawriter.writerow([str(name), str(desc), str(price1), str(price2), str(image)])
            # imprimimos el resultado
            #data['productos'].append({
            #    'name': name,
            #    'description': desc,
            #    'price1': price1,
            #    'price2': price2,
            #    'image': image
            #})

            TOTAL+=1

        #with open('data.txt', 'w') as outfile:
        #    json.dump(data, outfile)

        print(TOTAL)

        try:
            np+=1
            number="&page="+str(np)
            pagination = list(set([ x["href"] for x in html.find("ul",{"class" : "pagination pull-right"}).findAll("a",href=True) if number in x["href"]]))[0]
            grocery(URL_BASE.format(pagination),np)
        except Exception as e:
            pass

grocery(URL)
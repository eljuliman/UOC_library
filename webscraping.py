from urllib.request import urlopen

from bs4 import BeautifulSoup
import re
import requests
import time
import lxml
import pandas as pd

#Identificación de variables

URL_UOC = 'http://openaccess.uoc.edu'
INIT = '/webapps/o2/handle/10609/48236'
statusCode = 200
addvalue = []
diccionario = {}

while statusCode == 200:
    url = URL_UOC + INIT
    print (url)
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'lxml')
    for h in soup.find_all('strong'):
        a = h.find_all('a')
        for p in a:
            link = URL_UOC+p['href']
            titulo = p.getText()
            diccionario.update({titulo:link})
    print("fin bucle control ")

#Inicio de gestión de navegación

    for h in soup.find_all('div', {"class": "prev-next-links"}):
        tager = h.find_all('a')
        for p in tager:
            print(p['href'])
            INIT = p['href']
    # Insertamos los links de página en un vector para controlar el fin de páginas
    if (p['href']) in addvalue:
        print("Fin de páginas")
        break
    else:
        addvalue.append(p['href'])
    time.sleep(5)
    print(addvalue)

#Paso de lista a dataFrame y csv
print(diccionario)
df = pd.DataFrame([[key, diccionario[key]] for key in diccionario.keys()], columns=['Titulo', 'link'])
print(df)
df.to_csv(r'/Users/jmlejarza/Desktop/EXTRACT/data_csv.csv', index = False, header=True)


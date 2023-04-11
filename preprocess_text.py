# import library
from bs4 import BeautifulSoup
import requests
# Request to website and download HTML contents
url='https://www.lazada.sg/catalog/?_keyori=ss&from=input&q=mask'
req=requests.get(url)
content=req.text

soup=BeautifulSoup(content)
from bs4 import BeautifulSoup
from pandas.core.indexes import category  
import requests
import pandas as pd


#creacion 

titles = []
prices= []
stocks = []
cats = []
covers = []
descriptions= []
upcs = []
product_types = []
Price_excls = []
price_inclss = []
taxs = []
availabilitys = []
number_of_reviewss = []

#paginas

pages_to_scrape=50
for i in range (1,pages_to_scrape+1):
    url = f'https://books.toscrape.com/catalogue/page-{i}.html'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    articles = soup.find_all('article', class_="product_pod")


# el link al libro


    for article in articles:
        href = article.a['href']  
        url_book = f"http://books.toscrape.com/catalogue/{href}"

# entramos al link de cada libro  
      
        page = requests.get(url_book) 
        soup = BeautifulSoup(page.content, 'html.parser')

        info_div = soup.find('div', class_="product_main")

#title  
        title = info_div.h1.text
        titles.append(title)
#price        
        price = info_div.find('p', class_= "price_color").text
        prices.append(price)
#stock      
        stock = info_div.find('p', class_="instock availability").text.strip()
        stocks.append(stock)
#category
        ul_category = soup.find('ul', class_="breadcrumb")
        lis = ul_category.find_all('li')[2].a.text
        cats.append(lis)

       
#cover
        link = soup.find('div', class_="item active").img['src'][5:]
        cover = f"http://books.toscrape.com{link}"
        covers.append(cover)


        table = soup.find('table', class_="table-striped")
        trs = table.find_all('tr')
#product description
        description = soup.find('div', class_="sub-header").p 
        descriptions.append(description)    
#upc
        upc = trs[0].td.text
        upcs.append(upc)
#product type    
        product_type = trs[1].td.text
        product_types.append(product_type)

#price excl       
        Price_excl = trs[2].td.text
        Price_excls.append(Price_excl)
#price incl       
        price_incl = trs[3].td.text
        price_inclss.append(price_incl)
#tax       
        tax = trs[4].td.text
        taxs.append(tax)
#availabilit
        availability = trs[5].td.text
        availabilitys.append(availability)

#number of reviews
        number_of_reviews = trs[6].td.text
        number_of_reviewss.append(number_of_reviews) 
        
        books = pd.DataFrame({'title':titles,'price':prices,'stock':stocks,'category':cats,'cover':covers,'upc':upcs,'product type':product_types,'price excl':Price_excls,'price incl':price_inclss,'tax':taxs,'availabilit':availabilitys,'number of reviews':number_of_reviewss})
        books.index+=1
        print (books)
        
        books.to_csv('bookstext.csv')
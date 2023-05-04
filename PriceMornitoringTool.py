import sys
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd


class PriceMonitoringTool(object):
     def __init__(self, book_name):
          self.link = 'http://books.toscrape.com/'
          self.response = requests.get(self.link)
          self.soup = BeautifulSoup(self.response.content, 'html.parser')
          self.book_name = book_name

     def run(self):
          self.connCheck(self.response)
          cat_url = self.getCategoryURL(self, self.soup)
          self.parseCategory(self,self.soup,cat_url)
          product_url = self.findProdPage(self,self.response,book_name)
          book_info = self.getInfo(self,product_url)
          self.expCSV(self,product_url,book_info)
          
     def connCheck(self,url):
            if url.status_code != 200:
                print("Error fetching the book page")
                sys.exit()
 
     def getCategoryURL(self,soup,category=None):
          """
          Function that extracts catergory  
          """
          # get the URL of the category page 
          soup.select_one('.nav-list > li > ul > li').get_text().strip()
          for item in soup.select('.nav-list > li > ul > li'):
               itemText = item.get_text().strip()
               if itemText == category or category == None:
                    cat_url = item.a.get('href')
          return cat_url

     def parseCategory(self,soup,cat_url):
          """
          Function that checks all pages for a given catergory and generates category URL for all pages.  
          """
          products = []
          catlink = f"{soup}{cat_url}"
          catInfo = requests.get(catlink)
          catSoup = BeautifulSoup(catInfo.content, 'html.parser')
          hasMore = catSoup.select_one('.next')
          if hasMore:
               nextUrl = hasMore.a.get('href')
               cat_url = "/".join(cat_url.split("/")[0:-1]) + "/" + nextUrl
               products.extend(self.parseCategory(soup,cat_url))
          return products
     

     def findProdPage(self,soup,book_name):
        """
        Function that will check if books is available on the webpage and retrives book's product page url, 
        """
        # get the URL of the product page 
        if soup.find("a", {"title": book_name}):
          target_link = soup.find("a", {"title": book_name})
          product_url = target_link['href']
          return product_url
        else:
          print(f" Book {book_name} is not found on this website.")
          sys.exit()

     def getInfo(self,product_url): 
        """
           Get book product info, including:
           upc,book_title ,price_including_tax,price_excluding_tax,quantity_available,product_description,category,review_rating,image_url
        """
        # make a GET request to the product page
        product_page_response = requests.get('http://books.toscrape.com/' + product_url)
        # create a BeautifulSoup object to parse the HTML content of the product page
        product_soup = BeautifulSoup(product_page_response.content, 'html.parser')

        # scrape the desired information from the product page
        upc = product_soup.select_one('.table-striped > tr:nth-of-type(1) > td').get_text()
        book_title = product_soup.select_one('h1').get_text()
        price_including_tax = product_soup.select_one('.table-striped > tr:nth-of-type(4) > td').get_text()
        price_excluding_tax = product_soup.select_one('.table-striped > tr:nth-of-type(3) > td').get_text()
        quantity_available = product_soup.select_one('.table-striped > tr:nth-of-type(6) > td').get_text()
        product_description = product_soup.select_one('.product_page > p').get_text()
        category = product_soup.select_one('.breadcrumb > li:nth-of-type(3) > a').get_text()
        review_rating = product_soup.select_one('.star-rating')['class'][1]
        image_url = 'http://books.toscrape.com' + product_soup.find('img')['src'][5:]
        return upc, book_title, price_excluding_tax, price_including_tax, quantity_available, product_description,category,review_rating,image_url

     def expCSV(self,product_url,book_info):
          """
          export book info into CSV file
          """
          prod_url = 'http://books.toscrape.com/' + product_url
          df1 = pd.DataFrame({'product_page_url': [prod_url]})
          df2 = pd.DataFrame([book_info],columns=['UPC', 'book_title', 'price_including_tax', 'price_excluding_tax', 'quantity_available',
                              'product_description','category','review_rating','image_url'])
          final_df = pd.concat([df1, df2], axis=1)
          final_df.to_csv('book_info.csv')

if __name__ == "__main__":
     if len(sys.argv) != 2:
          print("You must provide book name")
          sys.exit(1)
     
     book_name = sys.argv[1]
     
     mornitoringTool = PriceMonitoringTool(book_name)
     mornitoringTool.run()
          


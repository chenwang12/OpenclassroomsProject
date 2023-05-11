import sys, os, shutil
import math
import string
import argparse
import requests
from bs4 import BeautifulSoup
import pandas as pd


class PriceMonitoringTool(object):
     def __init__(self):
          self.weblink = 'http://books.toscrape.com/'
          self.img_folder = os.path.join(os.path.join(os.environ['USERPROFILE'], 'Desktop'),'web_book_img')
          self.output_folder = os.path.join(os.path.join(os.environ['USERPROFILE'], 'Desktop'),'web_book_scrapping')

     def run(self, book_name=None, category=None):
          response = requests.get(self.weblink)
          self.connCheck(response)
          if book_name != None and category==None:
               product_url = self.findProdPage(book_name=book_name)
               book_info = self.getInfo(product_url)
               data_df = self.expCSV(product_url, book_info)
               self.downloadImg(data_df)
          else:
               product_url = self.findProdPage(book_name=book_name)
               cat_url = self.getCategoryURL(category)
               book_info = self.getInfo(cat_url)
               data_df = self.expCSV(product_url, book_info)
               self.downloadImg(data_df)
               
     def connCheck(self,response):
            """
            Function that checks if the network connection is OK
            """
            if response.status_code != 200:
                print("Error fetching the book page")
                sys.exit()  

     def getSoup(self,link=""):
          """
          Function that creates soup object for a given URL
          return: soup object
          """
          url = self.weblink + link
          response = requests.get(url)
          soup = BeautifulSoup(response.content, 'html.parser')
          return soup

     def findProdPage(self,link="",book_name=None):
        """
        Function that will retrive a book's product page url if book's name is specified,
        or will retrive all books' product page url 
        return: a list contains books' urls      
        """
        soup = self.getSoup(link)
        product_url = []
        hasMore = soup.select_one('.next')
        # get the URL of the product page 
        if book_name == None:
               product_urls = soup.find_all('a',href = True,title=True)
               # find href attributes of each book product
               for target_link in product_urls:
                    url = target_link["href"]
                    while "../" in url:
                         url = url.replace("../", "")
                    while "./" in url:
                         url = url.replace("./", "")
                    if not "catalogue" in url:
                         product_url.append("catalogue/" + url)    
                    else:
                         product_url.append(url)
        elif soup.find("a", {"title":string.capwords(book_name)}):
               target_link = soup.find("a", {"title":string.capwords(book_name)})
               if not "catalogue" in target_link["href"]:
                    product_url.append("catalogue/" + target_link["href"])
               else:
                    product_url.append(target_link["href"])
               return product_url
          # find href on all pages
        if hasMore:
               nextUrl = hasMore.a.get('href')
               product_url.extend(self.findProdPage(nextUrl,book_name))
        elif book_name != None:
             print(f"Warning: book {book_name} not found!")
        return product_url
     
     def getCategoryURL(self,category=None):
          """
          Function that extracts category URL for a given category or all categories in this website
          return: a list of category URLs
          """
          if category == None:
               product_url = self.findProdPage()
               return product_url
          else:
               # get the URL of the category page 
               cat_url_list = []
               # get the URL of the product page 
               soup = self.getSoup()
               #soup.select_one('.nav-list > li > ul > li').get_text().strip()
               for item in soup.select('.nav-list > li > ul > li'):
                     itemText = item.get_text().strip()
                     if itemText == category:
                         cat_url = item.a.get('href')
                         if cat_url != "":
                              cat_url_list.append(cat_url)                
                     for curl in cat_url_list:                    
                         results = self.findProdPage(curl)
               return results

     def getInfo(self,product_url): 
        """
           Get book product info, including:
           upc,book_title ,price_including_tax,price_excluding_tax,quantity_available,product_description,category,review_rating,image_url
        """
        productsInfo = []
        for product in product_url:
                # create a BeautifulSoup object to parse the HTML content of the product page
                product_soup = self.getSoup(product)
                # scrape the desired information from the product page
                category = product_soup.select_one('.breadcrumb > li:nth-of-type(3) > a').get_text()
                upc = product_soup.select_one('.table-striped > tr:nth-of-type(1) > td').get_text()
                book_title = product_soup.select_one('h1').get_text()
                price_including_tax = product_soup.select_one('.table-striped > tr:nth-of-type(4) > td').get_text()
                price_excluding_tax = product_soup.select_one('.table-striped > tr:nth-of-type(3) > td').get_text()
                quantity_available = product_soup.select_one('.table-striped > tr:nth-of-type(6) > td').get_text()
                product_description = product_soup.select_one('.product_page > p').get_text()
                review_rating = product_soup.select_one('.star-rating')['class'][1]
                image_url = 'http://books.toscrape.com' + product_soup.find('img')['src'][5:]
                productsInfo.append((category, upc, book_title, price_excluding_tax, price_including_tax, quantity_available, product_description, review_rating, image_url))
        return productsInfo

     def expCSV(self,product_url,book_info):
          """
          Export books' information of each category into a seperated csv file
          """
          output_folder = self.output_folder
          prod_url = [self.weblink + purl for purl in product_url]
          df1 = pd.DataFrame({'product_page_url': prod_url})
          df2 = pd.DataFrame(book_info,columns=['Category', 'UPC', 'Book_Title', 'Price_Including_Tax', 'Price_Excluding_Tax', 'Quantity_Available',
                              'Product_Description','Review_Rating','Image_url'])
          final_df = pd.concat([df1, df2], axis=1)
          categories = set(final_df['Category'])
          # create folder for saving output
          if os.path.exists(output_folder):
               shutil.rmtree(output_folder)
               os.makedirs(output_folder)                     
          else: 
               os.makedirs(output_folder)
          # save each category into a sperated csv file
          for cat in categories:
               if cat == math.nan:
                    return 0
               else:
                    cat_df = final_df[final_df['Category']==cat] 
                    cat_df.to_csv(f"{output_folder}/{cat}.csv")  
          return final_df   

     def downloadImg(self,data_df):
          """
          Function that download book cover images and save to the folder. Default folder is Desktop/web_book_img
          """
          # make a folder for saving images
          img_folder = self.img_folder
          if os.path.exists(img_folder):
               shutil.rmtree(img_folder)
               os.makedirs(img_folder)                     
          else: 
               os.makedirs(img_folder)
          for i, image in enumerate(data_df['Image_url']):    
               img_data = requests.get(image).content
               with open(f"{img_folder}/images{i}.jpg", 'wb') as handler:
                    handler.write(img_data)

if __name__ == "__main__":
     parser = argparse.ArgumentParser(description='This is a program to extract online book information')
     # Add arguments for system parameters
     parser.add_argument('-b','--book', type=str, default=None, help="Book's name to extract")
     parser.add_argument('-c','--category', type=str, default=None, help="Category to extract")
     args = parser.parse_args()
     # Access and use the system parameters
     book_name = args.book
     category = args.category
     
     mornitoringTool = PriceMonitoringTool()
     mornitoringTool.run(book_name,category)
          


import sys, os, shutil
import string
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd


class PriceMonitoringTool(object):
     def __init__(self, book_name):
          self.link = 'http://books.toscrape.com/'
          #self.response = requests.get(self.link)
          #self.soup = BeautifulSoup(self.response.content, 'html.parser')
          #self.book_name = book_name
          self.img_folder = os.path.join(os.environ['USERPROFILE'], 'Desktop') 
          self.img_folder = os.path.join(os.path.join(os.environ['USERPROFILE'], 'Desktop'),'web_book_img')

     def run(self, book_name=None):
          response = requests.get(self.link)
          #self.book_name = book_name
          self.connCheck(response)
          soup = BeautifulSoup(response.content, 'html.parser')
          cat_url = self.getCategoryURL(soup)
          self.parseCategory(self.link,cat_url)
          product_url = self.findProdPage(self.link,soup,book_name)
          book_info = self.getInfo(self.link,product_url)
          self.expCSV(self.link,product_url,book_info)
          
     def connCheck(self,url):
            """
            Function that checks if the network connection is OK
            """
            if url.status_code != 200:
                print("Error fetching the book page")
                sys.exit()
 
     def getCategoryURL(self,soup,category=None):
          """
          Function that extracts category URL for a given category or all categories in this website
          """
          # get the URL of the category page 
          cat_url_list = []
          # get the URL of the product page 
          soup.select_one('.nav-list > li > ul > li').get_text().strip()
          #print(target_cat)
          for item in soup.select('.nav-list > li > ul > li'):
               #print(item)
               itemText = item.get_text().strip()
               if itemText == category or category == None:
                    cat_url = item.a.get('href')
                    cat_url_list.append(cat_url)            
                    #print(cat_url_list)
          return cat_url_list
                  
          # cat_url = getCategoryURL(soup)
          # total = 0
          # for curl in cat_url:                                     ##### Parts need to be tested
          # pageUrl = weblink + curl
          # next_page = requests.get(pageUrl)
          # next_soup = BeautifulSoup(next_page.content, 'html.parser')
          # results = findProdPage(weblink, next_soup)
          # total += len(results)
          # print(total)

     # def parseCategory(self,link,cat_url):
     #      """
     #      Function that generates category URL for all pages.  
     #      """
     #      catlink = f"{link}{cat_url}"
     #      products = [catlink]
     #      catInfo = requests.get(catlink)
     #      catSoup = BeautifulSoup(catInfo.content, 'html.parser')
     #      hasMore = catSoup.select_one('.next')
     #      if hasMore:
     #            nextUrl = hasMore.a.get('href')
     #            catUrl = "/".join(cat_url.split("/")[0:-1]) + "/" + nextUrl
     #            products.extend(self.parseCategory(link, catUrl))
     #      return products

     def findProdPage(self,link,soup,book_name=None):
        """
        Function that will retrive a book's product page url if book name is specified,
        or will retrive all books' product page url 
        """
        product_url = []
        hasMore = soup.select_one('.next')
        # get the URL of the product page 
        if book_name == None:
               product_urls = soup.find_all('a',href = True, title=True)
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
               print("HASMORE")
               nextUrl = hasMore.a.get('href')
               pageUrl = "/".join(link.split("/")[0:-1]) + "/" + nextUrl
               next_page = requests.get(pageUrl)
               next_soup = BeautifulSoup(next_page.content, 'html.parser')
               product_url.extend(self.findProdPage(pageUrl,next_soup, book_name))
        return product_url

     def getInfo(self,link,product_url): 
        """
           Get book product info, including:
           upc,book_title ,price_including_tax,price_excluding_tax,quantity_available,product_description,category,review_rating,image_url
        """
        productsInfo = []
        for product in product_url:
                # make a GET request to the product page
                product_page_response = requests.get(weblink + product)
                # create a BeautifulSoup object to parse the HTML content of the product page
                product_soup = BeautifulSoup(product_page_response.content, 'html.parser')

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
                #print(upc, book_title, price_excluding_tax, price_including_tax, quantity_available, product_description, category, review_rating, image_url)
                productsInfo.append((category, upc, book_title, price_excluding_tax, price_including_tax, quantity_available, product_description, review_rating, image_url))
        return productsInfo

     def expCSV(self,link,product_url,book_info):
          """
          export book info into CSV file
          """
          prod_url = [link + purl for purl in product_url]
          df1 = pd.DataFrame({'product_page_url': prod_url})
          df2 = pd.DataFrame(book_info,columns=['Category', 'UPC', 'Book_Title', 'Price_Including_Tax', 'Price_Excluding_Tax', 'Quantity_Available',
                              'Product_Description','Review_Rating','Image_url'])
          final_df = pd.concat([df1, df2], axis=1)
          categories = set(final_df['Category'])
          for cat in categories:
               cat_df = final_df[final_df['Category']==cat] 
               cat_df.to_csv(f"{cat}.csv")     

     def downloadImg(url,final_df,img_folder):
          """
          Function that download book cover images and save to the folder. Default folder is Desktop/web_book_img
          """
          img_data = requests.get(url).content
          if os.path.exists(img_folder):
                    shutil.rmtree(img_folder)
                    os.makedirs(img_folder)                
          else: 
                    os.makedirs(img_folder)
          final_df['']
          #for i, image in enumerate(images):
               #with open(f"{image_folder}/images{i+1}.jpg", 'wb') as handler:
          with open(f"{img_folder}/images{1}.jpg", 'wb') as handler:
                         handler.write(img_data)

if __name__ == "__main__":
     if len(sys.argv) != 2:
          print("You must provide a book name")
          sys.exit(1)
     
     book_name = sys.argv[1]
     
     mornitoringTool = PriceMonitoringTool(book_name)
     mornitoringTool.run()
          


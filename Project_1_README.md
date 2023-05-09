## Price Mornitoring System
### Project Description
 
The purpose of this python script is to obtain book information from website [Books to Scrape](http://books.toscrape.com/index.html). 

Key information that will be extracted for each book:
* product_page_url
* universal_ product_code (upc)
* book_title
* price_including_tax
* price_excluding_tax
* quantity_available
* product_description
* category
* review_rating
* image_url 
* book cover in jpeg format

### Prerequisites
* Python 3.5 +
* library: BeautifulSoup, pandas 

### How to run the script
You can extract one single book information by passing optional argument <mark>--b</mark> \
or you can extract all books information for a given category by pass optional argument <mark>--c</mark> \
or without passing any optional argument, the script will extract all books' information on this website. \
Example: 
* To extract information of book "Soumission": \
``` python PriceMornitoringTool.py --b soumission ```
* To extract all books information of category "Fantasy" \
``` python PriceMornitoringTool.py --c Fantasy ```
* To extract all books information on this website \
``` python PriceMornitoringTool.py ```

### Output
* Information will be saved to folders on your PC Desktop: 
    * "web_book_scrapping": storing book information
    * "web_book_img": storing images
* Book information is saved as an indivial CSV file for each category
 
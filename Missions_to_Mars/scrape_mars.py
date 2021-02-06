# Dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
import time
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": 'c:\windows\chromedriver'}
    return Browser("chrome", **executable_path, headless=False)

# 
def scrape():

    mars_scrape = {}

    # URL of page to be scraped
    news_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

    # Retrieve page with the splinter
    
    executable_path = {'executable_path': 'c:\windows\chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(news_url)
    time.sleep(2)  # sleep until you know it is loaded
    html = browser.html

    # Create BeautifulSoup object; parse with 'html.parser'
    news_soup = bs(html, 'html.parser')

    # Collect the latest News Title and Paragraph Text
    # pull back first news title on page
    results = news_soup.find('li', class_='slide')
    
    # try and error surrounding looking for the requested items

    for result in results:
        # Error handling
        try:
            # Identify and return title of news article
            news_title = result.find('div', class_='content_title').text.strip()

            # Identify and return paragraph text
            news_p = result.find('div', class_='article_teaser_body').text.strip()
            print(f'{news_title}: {news_p}')

        except Exception as e:
            print(e)

    # Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the 
    # planet including Diameter, Mass, etc.

    # URL of page to be scraped
    facts_url = 'https://space-facts.com/mars/'

    # Use pandas to return contents of all tables in page
    tables_df = pd.read_html(facts_url)
    
    # Isolate Mars facts table -- first one on page
    facts_df = tables_df[0]
    
    # Convert Dataframe to html 
    facts = facts_df.to_html()

    # Strip newline characters.
    html_facts = facts.replace('\n', '')

    # Mars Hemispheres

    landing_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    executable_path = {'executable_path': 'c:\windows\chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(landing_url)
    time.sleep(2)  # sleep until you know it is loaded
    html = browser.html 
    # Create BeautifulSoup object; parse with 'html.parser'
    landing_soup = bs(html, 'html.parser')

    # Collect the links from the scraped results

    hemi_results = landing_soup.find_all('a', class_='itemLink product-item')

    links = []
    for link in hemi_results:
        full_link = link.get('href')
        links.append(full_link)

    # Make sure you have no duplicates
    end_links = list(set(links))

    # click each of the links to the hemispheres in order to find the image url to the full resolution image.

    link_start = 'https://astrogeology.usgs.gov'
    hemisphere_image_urls = []
    for link in end_links:
        # To store the link and title
        hemi_dict = {}
        browser = Browser('chrome', **executable_path, headless=True)
        hemi_url = f"{link_start}{link}"
        browser.visit(hemi_url)
        html = browser.html
        time.sleep(2)  # sleep until you know it is loaded

        #Save image url string Hemisphere title containing the hemisphere name. Keys: img_url, title
        image_soup = bs(html, 'html.parser')
    
        # Get the title
        try:
            title_result = image_soup.find('h2', class_='title').text.strip()

        except Exception as e:
            pass
    
        # Get the img
        try: 
            image_link = image_soup.find('div', class_='downloads').li.a["href"]

        except:
            pass
        
        hemi_dict.update({"title": title_result, "img_url": image_link})
        hemisphere_image_urls.append(hemi_dict)
    
    mars_scrape = {'news_title': news_title,
                    'news_p': news_p, 
                    'facts': html_facts,
                    'hemis': hemisphere_image_urls}

    return mars_scrape
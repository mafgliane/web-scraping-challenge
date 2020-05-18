# Import dependencies
import pandas as pd
import os
import pymongo
import requests
from bs4 import BeautifulSoup as bs
from splinter import Browser
import time

wait_time=5

# # Create global dictionary that can be imported into Mongo
# mars_info = {}

def init_browser():
    #pointing to the directory where chromedriver exists
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

# NASA MARS NEWS
def scrape_mars_news():
    
    # Initialize browser 
    browser = init_browser()

    # Visit Nasa news url through splinter module
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(sleep_time)

    # HTML Object
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')

    # Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text
    news_title = soup.find('div', class_='content_title').find('a').text
    news_p = soup.find('div', class_='rollover_description_inner').text

    # Dictionary entry from MARS NEWS
    mars_info['news_title'] = news_title
    mars_info['news_paragraph'] = news_p

    browser.quit()
    # return mars_info

 

# JPL MARS SPACE IMAGES - FEATURED IMAGE
def scrape_mars_image():

    # Initialize browser 
    browser = init_browser()

    # Visit Mars Space Images through splinter module
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)
    time.sleep(sleep_time)

    # HTML Object 
    html_image = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html_image, 'html.parser')

    # Retrieve background-image url from style tag 
    featured_image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

    # Concatenate website url with scrapped route
    featured_image_url = 'https://www.jpl.nasa.gov' + featured_image_url

    # Display full link to featured image
    featured_image_url 

    # Dictionary entry from FEATURED IMAGE
    mars_info['image_url'] = featured_image_url 
        
    browser.quit()

    # return mars_info

        

# MARS WEATHER
def scrape_mars_weather():
    # Initialize browser 
    browser = init_browser()

    #browser.is_element_present_by_css("div", wait_time=1)

    # Visit Mars Weather Twitter through splinter module
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)
    time.sleep(sleep_time)

    # HTML Object 
    html_weather = browser.html

    # Parse HTML with Beautiful Soup
    weather_soup = bs(html_weather, 'html.parser')

    # Find all elements that contain tweets
    latest_tweets = weather_soup.find_all('span')

# Search for weather related tweets only
    for tweet in latest_tweets: 
        if  'InSight sol' in tweet.text:
            mars_weather = tweet.text
            break
        else: 
            pass
             
    # Dictionary entry from WEATHER TWEET
    mars_info['mars_weather'] = mars_weather

    browser.quit()

    # return mars_info

   
# MARS FACTS
def scrape_mars_facts():

    # Initialize browser 
    browser = init_browser()

    facts_url = 'http://space-facts.com/mars/'
    browser.visit(url)
    time.sleep(sleep_time)

    # Use Pandas to "read_html" to parse the URL
    table = pd.read_html(url)
    #Find Mars Facts DataFrame in the lists of DataFrames
    df = tables[0]
        
    #define the columns
    df.columns = ['Description', 'Data']
    
    #Convert the data to an HTML table string
    html_table = df.to_html(table_id="html_tbl_css",justify='left',index=False)
    html_table = html_table.replace("\n","")

    # Dictionary entry from MARS FACTS
    mars_info['table'] = html_table

    browser.quit()

    # return mars_info


# MARS HEMISPHERES

def scrape_mars_hemispheres():

    # Initialize browser 
    browser = init_browser()

    # Visit hemispheres website through splinter module 
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    # response = requests.get(hemisphere_url)
    browser.visit(hemisphere_url)
    time.sleep(sleep_time)
    soup = bs(response.text, 'html.parser')
  
    # Retreive all items that contain mars hemispheres information
    items = soup.find_all('div', class_='item')

    # Create empty list for hemisphere urls 
    hemisphere_image_urls = []
    main_url = 'https://astrogeology.usgs.gov' 

    # Loop through the items previously stored
    for i in items: 
        title = i.find('h3').text
        partial_img_url = i.find('a', class_='itemLink product-item')['href']
        browser.visit(main_url + partial_img_url)
        partial_img_html = browser.html
            
        soup = bs( partial_img_html, 'html.parser')
        img_url = main_url + soup.find('img', class_='wide-image')['src']
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})

    # Dictionary entry from MARS HEMMISPERES
    mars_info['hemisphere_img_urls'] = hemisphere_image_urls

    browser.quit()

    # return mars_info

if __name__ == "__main__": 
    scrape_mars_news()
    print(mars_info)
    print()
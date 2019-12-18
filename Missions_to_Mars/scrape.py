from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import re

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape_mars():
    browser = init_browser()
    hemisphere =[]
    hemisphere_list=['Cerberus','Schiaparelli','Syrtis','Valles']
    for hemi in hemisphere_list:
        hemispheres={}
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url)
        html = browser.html
        soup = bs(html,'html.parser')
        browser.click_link_by_partial_text(hemi)
        html = browser.html
        soup = bs(html,'html.parser')
        hemispheres['image']=soup.find('a',target="_blank")['href']
        hemispheres['title']=soup.find('h2',class_="title").text
        hemisphere.append(hemispheres)
    browser.quit()
    
    browser = init_browser()

    # Visit mars
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = bs(html, "html.parser")

    news_title = soup.findAll("div",{"class":"content_title"})[0].text.strip(' \t\n')
    news_p = soup.findAll("div",{"class":"rollover_description"})[0].text.strip(' \t\n')
    nasaData = {
        "news_title": news_title,
        "news_teaser": news_p
    }
    
    browser.quit()
    
    browser = init_browser()
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = bs(html, "html.parser")

    mars_weather = soup.find("div",{"class":"js-tweet-text-container"}).p.text
    mars_weather_clean = re.sub(r'(\s+|\n+|InSight|pic.twitter.com/J9DKptw2oo)', ' ', mars_weather)
    
    browser.quit()
    
    browser = init_browser()
    
    url_base = "https://www.jpl.nasa.gov"
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = bs(html, "html.parser")

    feature_mars = soup.find("div",{"class":"carousel_items"})
    relative_feature_image = feature_mars.a["data-fancybox-href"]
    feature_image = url_base + relative_feature_image
    feature_image_description = feature_mars.a["data-description"].strip('\r\t\n')
    feature_image_title = feature_mars.h1.text.strip('\r\t\n')

    marsData = {
        "feature_image": feature_image,
        "feature_image_title": feature_image_title,
        "feature_image_description": feature_image_description
    }
    
    browser.quit()
    
    dataPage = {"hemisphere":hemisphere,"nasaData":nasaData,"weatherData":mars_weather_clean,"featuredImage":marsData}
    return dataPage



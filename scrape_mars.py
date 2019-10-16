
import pandas as pd   
from splinter import Browser   
from bs4 import BeautifulSoup as bs
import requests as req     
import time
import pymongo


def init_browser():
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)      

def scrape():
    # browser = init_browser()
    #___NN Nasa News  
    browser = Browser('chrome', headless=False)
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(1)
    html = browser.html 
    nasa_soup = bs(html, 'html.parser')
    nntitle = nasa_soup.find("div", class_="content_title").text
    nnparagraph = nasa_soup.find("div", class_="article_teaser_body").text

    #___Mars JPL Image Feature
    #browser.visit('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')
    #time.sleep( 1 )
    #image_url = browser.find_by_css("full_image")
    browser.visit('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')
    time.sleep( 1 )
    html = browser.html
    soup = bs(html, "html.parser")
    theimage = soup.find("img", class_="thumb")["src"]
    image_url = "https://www.jpl.nasa.gov" + theimage

    #___Mars Weather
    browser.visit('https://twitter.com/marswxreport?lang=en')
    time.sleep( 1 )
    tweet_html = browser.html                                                   
    tweet_soup = bs(tweet_html, 'html.parser')                                  
    mars_weather = tweet_soup.find('p',class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text

    #___Mars Facts    
    factsurl = 'https://space-facts.com/mars/'
    time.sleep( 1 )
    tables = pd.read_html(factsurl)
    df = tables[0]
    df.columns = ['Mars - Earth Comparison', 'Mars', 'Earth']
    df.set_index('Mars - Earth Comparison', inplace=True)
    html_table = df.to_html(index = True, header =True)

    #___Mars  hemisperes   
    ImageURLs = []
    browser.visit('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars')
    time.sleep( 1 )
    CerberusHemisphereEnhanced = browser.find_by_text('Cerberus Hemisphere Enhanced')
    cerber = CerberusHemisphereEnhanced.click()        #returns the Browser.url
    ImageURLs.append(browser.url)

    browser.visit('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars')
    SchiaparelliHemisphereEnhanced = browser.find_by_text('Schiaparelli Hemisphere Enhanced')
    SchiaparelliHemisphereEnhanced.click()             #returns the Browser.url
    ImageURLs.append(browser.url)

    browser.visit('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars')
    SyrtisMajorHemisphereEnhanced = browser.find_by_text('Syrtis Major Hemisphere Enhanced')
    SyrtisMajorHemisphereEnhanced.click()
    ImageURLs.append(browser.url)

    browser.visit('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars')
    VallesMarinerisHemisphereEnhanced = browser.find_by_text('Valles Marineris Hemisphere Enhanced')
    VallesMarinerisHemisphereEnhanced.click()
    ImageURLs.append(browser.url)


    # Mars Info Dictionary
    scrapeddata = {"mars_news":nntitle,"mars_paragraph":nnparagraph,"mars_image":image_url,"mars_weather":mars_weather,"mars_facts":html_table,"mars_hemisphere":ImageURLs}

    browser.quit()
    return scrapeddata

#some_variable = scrape()    #here for testing

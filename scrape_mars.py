#!/usr/bin/env python
# coding: utf-8

from splinter import Browser
from bs4 import BeautifulSoup
from datetime import datetime
import requests
from pprint import pprint
import time


executable_path = {"executable_path": "driver/chromedriver.exe"}
browser = Browser("chrome", **executable_path, headless=True)


def scrape():
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, "html5lib")
    for i in range(10):
        try:
            first_article = soup.find(
                "div", class_="image_and_description_container")

            news_title = first_article.find("div", class_="content_title").text
            news_title

            news_p = first_article.find(
                "div", class_="article_teaser_body").text
            news_p
        except:
            time.sleep(.5)
            print("this failed")
        else:
            break

    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    browser.click_link_by_partial_text('FULL IMAGE')
    browser.click_link_by_partial_text('more info')
    browser.find_by_css('.main_image').click()

    featured_image_url = browser.url
    featured_image_url

    url = "https://twitter.com/marswxreport?lang=en"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")

    mars_weather = soup.find(
        'p', class_="js-tweet-text").text.split("pic.twitter")[0].split("InSight ")[-1]
    mars_weather

    url = "https://space-facts.com/mars/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")

    mars_facts_table = str(soup.find(id="tablepress-p-mars"))

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    hemisphere_image_urls = []
    for count in range(4):
        link = browser.find_link_by_partial_text('Hemisphere Enhanced')[count]
        link.click()
        title = browser.find_by_css('.title').first.text
        url = browser.find_by_text('Sample').first["href"]

        temp = {
            "title": title,
            "img_url": url
        }
        browser.back()
        hemisphere_image_urls.append(temp)

    return({
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "mars_facts_table": mars_facts_table,
        "hemisphere_image_urls": hemisphere_image_urls
    })

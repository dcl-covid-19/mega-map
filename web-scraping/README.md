# Web Scraping

This subdirectory contains all code related to web scrapers. The scrapers can be found in
the county-scraping subdirectory.

# Selenium and Webscraping

In some cases when executing a GET request, the data might not be available until some javascript
runs that will make an async request. To get around this limitation, we require the use of a webdriver to scrape to the content on the page. An example of such a script is CalfreshScraper.py.
import re
import csv
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from chromedriver_py import binary_path # this gets you the path variable

class CalfreshScraper(object):
    URL = "https://calfresh.dss.ca.gov/food/officelocator/"

    def __init__(self):
        """
        Initializes the web driver and waits for the page to load
        """
        self.driver = webdriver.Chrome(executable_path=binary_path)
        self.driver.get(self.URL)
        time.sleep(3)
    
    def scrape(self):
        """
        Scrapes the calfresh office website and saves the data to a CSV file
        """
        offices = self.get_calfresh_office_element_list()
        self.rows = self.parse_office_list(offices)
        self.save()
    
    def get_calfresh_office_element_list(self):
        """
        Searches for the calfresh offices HTML element, then extracts a 
        list of web elements each corresponding to a CalFresh office.
        """
        office_list = self.driver.find_element_by_id("calfresh-offices")
        offices = office_list.find_elements_by_class_name("calfresh_office")
        return offices
    
    def parse_office_list(self, offices):
        """
        Parses the list of web elements and returns a list of rows that
        will be used as rows in a CSV file
        """
        rows = []
        for office in offices:
            row = office.text.split("\n")

            # Substitute the links for the last 2 elements
            inner_html = office.get_attribute("innerHTML")
            elements = inner_html.split("<br>")

            for element in elements:
                if "a" in element and "href" in element:
                    soup = BeautifulSoup(element, features="html.parser")
                    url = soup.find_all("a")[0]["href"]
                    
                    if "Get Directions" in element:
                        row[5] = url
                    elif "Visit Website" in element:
                        row[6] = url
            
            rows.append(row)
        return rows
    
    def save(self):
        """
        Saves the content to a CSV in the Downloads directory.
        """
        writer = csv.writer(open("calfresh.csv", "w"))
        headers = ["Name", "Address", "County", "Hours", "Phone", "Directions", "Website"]
        
        writer.writerow(headers)
        for row in self.rows:
            writer.writerow(row)
        1/0
    
    def dispose(self):
        """
        Closes the webdriver in case an exception occurs
        """
        self.driver.close()

def main():
    scraper = CalfreshScraper()
    try:
        scraper.scrape()
    except Exception as error:
        print(error)
        scraper.dispose()

if __name__ == "__main__":
    main()
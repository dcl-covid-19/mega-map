import re
import csv
import time
from selenium import webdriver
from data_extraction_and_formatting.mapping.mapper import Mapper
from bs4 import BeautifulSoup
from chromedriver_py import binary_path # this gets you the path variable

class CalfreshScraper(object):
    URL = "https://calfresh.dss.ca.gov/food/officelocator/"
    ALL_WEEKDAYS = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

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
        self.dispose()
        self.hsds_rows = [
            self.calfresh_to_hsds_row(row)
            for row in self.rows
        ]
        # self.save()
        self.save_hsds()
    
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
    
    def save_hsds(self):
        """
        Saves the content to a CSV in the Downloads directory.
        """
        writer = csv.writer(open("hsds_calfresh.csv", "w"))

        writer.writerow(Mapper.csv_header())
        for row in self.hsds_rows:
            writer.writerow(row)

    @classmethod
    def short_weekday_to_day_index(cls, short_day):
        d = {
            "M": 0,
            "T": 1,
            "W": 2,
            "Th": 3,
            "F": 4,
            "S": 5,
            "Su": 6,
        }
        return d.get(short_day)

    @classmethod
    def abbv_weekday_to_day_index(cls, abbv_day):
        d = {
            "Mon": 0,
            "Tue": 1,
            "Wed": 2,
            "Thu": 3,
            "Thur": 3,
            "Fri": 4,
            "Sat": 5,
            "Sun": 6,
        }
        return d.get(abbv_day)

    @classmethod
    def day_index_to_weekday_string(cls, day_index):
        d = {
            0: "Monday",
            1: "Tuesday",
            2: "Wednesday",
            3: "Thursday",
            4: "Friday",
            5: "Saturday",
            6: "Sunday",
        }
        return d.get(day_index)

    @classmethod
    def calfresh_to_hsds_row(cls, row):
        (
            name,
            _,
            _,
            hours,
            _,
            _,
            _
        ) = row

        # Examples:
        #
        # "Hours: Mon - Fri 7:30 AM - 4:00 PM"
        # ["Hours: ", "Mon", "-", "Fri", "7:30", "AM", "-", "4:00", "PM"]
        #
        # Hours: 8:00a-5:00p
        # ["Hours: ", "8:00a-5:00p"]
        # 
        # Hours: 7:30a-5:30p (M-Th)
        # ["Hours: ", "7:30a-5:30p", "(M-Th)"]

        hours_tokens = hours.split(" ")
        opens_at = None
        closes_at = None
        add_hours = None
        weekdays = []
        skip_indices = set()
        for (i, hour_token) in enumerate(hours_tokens):
            if i in skip_indices:
                continue
            if re.search(r'\d', hour_token):
                if (
                    opens_at is not None
                    and closes_at is not None
                ):
                    if "-" in hour_token:
                        add_hours = hour_token
                    continue
                elif "-" in hour_token:
                    opens_at, closes_at = hour_token.split("-")
                    opens_at = opens_at.replace("a", " AM")
                    closes_at = closes_at.replace("a", " AM")
                    opens_at = opens_at.replace("p", " PM")
                    closes_at = closes_at.replace("p", " PM")
                elif i + 1 in range(len(hours_tokens)):
                    am_pm_string = hours_tokens[i + 1]
                    skip_indices.add(i + 1)

                    if opens_at is None:
                        opens_at = " ".join([hour_token, am_pm_string])
                    elif closes_at is None:
                        closes_at = " ".join([hour_token, am_pm_string])
                    else:
                        raise Exception(f"Invalid hours: {hours} {hour_token}")
            elif re.search(r"Mon|Tue|Wed|Thu|Fri", hour_token) is not None:
                if "-" in hour_token: # "Mon-Fri"
                    start_day, end_day = hour_token.split("-")
                    start_day_index = cls.abbv_weekday_to_day_index(start_day)
                    end_day_index = cls.abbv_weekday_to_day_index(end_day)
                    if start_day_index is None or end_day_index is None:
                        raise Exception(f"Invalid day: {hours} {hour_token}")

                    # range(1, 4) -> [1,2,3,4]
                    day_indices = list(range(start_day_index, end_day_index + 1))
                    weekdays = [
                        cls.day_index_to_weekday_string(day_index)
                        for day_index in day_indices
                    ]
                else: # Mon - Fri
                    if i + 2 not in range(len(hours_tokens)):
                        raise Exception(f"Invalid day: {hours} {hour_token}")
                    start_day = hour_token
                    end_day = hours_tokens[i + 2]
                    skip_indices.add(i + 2)

                    start_day_index = cls.abbv_weekday_to_day_index(start_day)
                    end_day_index = cls.abbv_weekday_to_day_index(end_day)
                    if start_day_index is None or end_day_index is None:
                        raise Exception(f"Invalid day: {hours} {hour_token}")

                    # range(1, 4) -> [1,2,3,4]
                    day_indices = list(range(start_day_index, end_day_index + 1))
                    weekdays = [
                        cls.day_index_to_weekday_string(day_index)
                        for day_index in day_indices
                    ]

            elif "(" in hour_token:
                hour_token = hour_token.replace("(", "")
                hour_token = hour_token.replace(")", "")
                start_day, end_day = hour_token.split("-")
                start_day_index = cls.short_weekday_to_day_index(start_day)
                end_day_index = cls.short_weekday_to_day_index(end_day)
                if start_day_index is None or end_day_index is None:
                    raise Exception(f"Invalid day: {hours}")

                # range(1, 4) -> [1,2,3,4]
                day_indices = list(range(start_day_index, end_day_index + 1))
                weekdays = [
                    cls.day_index_to_weekday_string(day_index)
                    for day_index in day_indices
                ]

        mapper = Mapper(
            name = name,
            id = None,
            weekday = ",".join(cls.ALL_WEEKDAYS if not weekdays else weekdays),
            opens_at = opens_at,
            closes_at = closes_at,
            add_hours = add_hours,
        )
        return mapper.to_csv_row()

    def dispose(self):
        """
        Closes the webdriver in case an exception occurs
        """
        self.driver.close()

def main():
    scraper = CalfreshScraper()
    scraper.scrape()

if __name__ == "__main__":
    main()
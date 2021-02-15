## Scraping Strategies 

### ArcGIS Maps

Often, county resources are listed on an ArcGIS map, like [this one](https://cocogis.maps.arcgis.com/apps/webappviewer/index.html?id=fea1f3021a50455495b7e7e11325ecd4) from Contra Costa.

#### Option 1: Scrape data from ArcGIS backend

Some ArcGIS map interfaces make it easy to get to the backend database. In the top right corner of the map, look for a "layers" icon (three stacked diamonds): <img src="https://i.ibb.co/2NsmTzz/Screen-Shot-2021-02-15-at-6-29-54-PM.png" width="30">

If it is present, clicking on the icon should reveal a list of the layers displayed on the map. This usually corresponds to different datasets. For the layers you are interested in scraping, click the three-dot icon to the right of the layer name, then click "Description" in the popup that appears.

<img src="https://i.ibb.co/V3xL9bq/Screen-Shot-2021-02-15-at-6-35-09-PM.png" width="300">

This should take you to a page with metadata about the dataset. Scroll to the bottom and find the "Query" link. Going to the "Query" link should lead you to an interface like this:

<img src="https://i.ibb.co/mXJSNVc/Screen-Shot-2021-02-15-at-6-42-54-PM.png" width="500">

This interface allows us to directly query the backend data that is being shown on the ArcGIS map frontend. Usually, we are interested in getting all the data -- to do so, enter the following query parameters:

- Where: 1=1 (this means "get all the data entries")
- Out Fields: * (this means "get all the data fields available for each entry")
- Format: JSON

Click the "Query (GET)" button, and you should be redirected to a page with the data in JSON format. You can then use a Python script to parse this JSON and format the data however you would like (ex. write to a CSV).

See Contra Costa County.ipynb for an example.

### Selenium

In some cases when executing a GET request, the data might not be available until some javascript runs that will make an async request. To get around this limitation, we require the use of a webdriver to scrape to the content on the page. An example of such a script is CalfreshScraper.py.

<a href="https://ibb.co/BrLwn5C"><img src="https://i.ibb.co/mXJSNVc/Screen-Shot-2021-02-15-at-6-42-54-PM.png" alt="Screen-Shot-2021-02-15-at-6-42-54-PM" border="0"></a>
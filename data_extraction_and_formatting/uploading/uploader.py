import json
import requests
import urllib

class Uploader(object):
    """
    An utility class used to upload data to airtable.
    """

    post_headers = {
        "Authorization" : "Bearer keyLBTgL8hjaceVN4",
        "Content-Type": "application/json"
    }

    def __init__(self, url):
        self.url = url
    
    def insert(self, url, header, data):
        print("Insered Data -> {0}".format(data))
        print ("."*40)
        response = requests.post(url, headers = header, data = json.dumps(data))
        print(response.text)
        _id = json.loads(response.text.encode('utf8'))["id"]
        print("Id -> "+str(_id) + "::: "+ url)
        print("Response     -> {0}".format(response.text))
        print("-"*80)
        return _id
    
    def get_or_create(self, url, header, data, unique_field_name):
        url_params = "?"+urllib.parse.urlencode({
            "maxRecords": 1,
            "filterByFormula": "{"+unique_field_name+"}='"+data["fields"][unique_field_name]+"'"
        })
        response = requests.get(url + url_params, headers = header)
        records = json.loads(response.text.encode('utf8'))["records"]
        if len(records) == 0:
            return self.insert(url, header, data)
        else:
            _id = json.loads(response.text.encode('utf8'))["records"][0]["id"]
            print("Existing Id -> "+str(_id) + "::: "+ url)
            return _id

class ScheduleUploader(object):
    def __init__(self):
        super.__init__(
            ScheduleUploader,
            url = 'https://api.airtable.com/v0/applQOkth8R2ns3qo/schedule'
        )
import requests
import csv

def fcnparse_opendays(stringopendays):
    print(stringopendays)

def fcnparse_siteaddress(full_address):
    tmp = full_address.split(', ')
    address = full_address#tmp[0]
    city = ""#tmp[1]
    tmp2 = ""#tmp[2].split(' ')
    state = ""#tmp2[0]
    zipcode = ""#tmp2[1]
    return address, city, state, zipcode

def fcnparse_opendays(attributesOPENDAYS):
    return ["Monday","Tuesday","Thursday"]


import requests
import csv

post_url_services = 'https://api.airtable.com/v0/applQOkth8R2ns3qo/services'
post_url_organizations = 'https://api.airtable.com/v0/applQOkth8R2ns3qo/organizations'
post_url_address = 'https://api.airtable.com/v0/applQOkth8R2ns3qo/address'
post_url_schedule = 'https://api.airtable.com/v0/applQOkth8R2ns3qo/schedule'

post_headers = {
    'Authorization' : 'Bearer keyFaCMgt8zX71GnJ',
    'Content-Type': 'application/json'
}

f = open('/Users/Ashwin/Documents/BAC/20200919cfsj/Santa Clara Scrape 10_1 - Food School Meal Sites .csv')
csv_f = csv.reader(f)

#Skip header row
count = 1
for row in csv_f:
    if count == 1:
        break

count = 1
for row in csv_f:
    #print(row)
    rowcount = 0
    for elem in row:
        print(rowcount, elem)
        rowcount = rowcount+1

    #Parse attributes.SITESCHOOLDISTRICT
    attributesSITESCHOOLDISTRICT = row[4]
    airtableSITESCHOOLDISTRICT = {"fields": {"name": attributesSITESCHOOLDISTRICT}}
    print((requests.post(post_url_organizations, headers = post_headers, json = airtableSITESCHOOLDISTRICT)).status_code)

    #Parse attributes.SITENAME
    attributesSITENAME = row[5]
    airtableSITENAME = {"fields": {"Name": attributesSITENAME}}
    print((requests.post(post_url_services, headers = post_headers, json = airtableSITENAME)).status_code)

    #Parse attributes.SITEADDRESS
    attributesSITEADDRESS = row[5]
    address, city, state, zipcode = fcnparse_siteaddress(attributesSITEADDRESS)
    print(address, city, state, zipcode)
    airtableSITEADDRESS = {"fields": {"address_1": address,"city": city,"State": state,"Zip Code": zipcode}}
    print((requests.post(post_url_address, headers = post_headers, json = airtableSITEADDRESS)).status_code)

    #Parse attributes.OPENDAYS
    attributesOPENDAYS = row[6]
    opendays = fcnparse_opendays(attributesOPENDAYS)
    airtableOPENDAYS = {"fields": {"weekday": opendays}}
    print((requests.post(post_url_schedule, headers = post_headers, json = airtableOPENDAYS)).status_code)


    if count == 1:
        break    

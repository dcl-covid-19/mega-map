# %%
#! opt/anaconda3/bin/python
import googlemaps
import pandas as pd

API_KEY = 'AIzaSyBsnyJeSZEoK3bvSq9M8jsmEsWJ8z9uV9A'
gmaps = googlemaps.Client(key = API_KEY)

df = pd.concat(pd.read_excel('snap_raw_all.xlsx', sheet_name = None), ignore_index = True)

# %%
# Improves search result success by removing words at the end of the site name that contain digits.
# Looking at the data, 7-Eleven produces inconsistencies so we add a special case to handle them.
import regex 

def trim_suffix(site_name):
    if not site_name:
        return site_name
    clean_name = regex.sub(pattern = "\W", repl = " ", string = site_name.lower())
    bits = clean_name.split(" ")
    while not str.isalpha(bits[-1]) and "eleven" not in bits[-1]:
        del bits[-1]
    return " ".join(bits)

# %%
# Returns a place id for closest match based on input cols.
# Returns none if there isn't a match.

def get_place_id(site_name, address, city, lon = "", lat = ""):
    search_string = " ".join([trim_suffix(site_name), address, city])
    coords = "".join(["point:", str(lon), ",", str(lat)])

    candidates = gmaps.find_place(
        input = search_string,
        input_type = "textquery",
        location_bias=coords,
    ).get('candidates')

    if not candidates:
        return None
    else: 
        return candidates[0].get('place_id')

# %% [markdown]
# ### Get attributes
# 
# Optimized for one read-through. We want:
# 
# * Lat and long coords
# * Hours
# * Zipcode
# * Phone number
# * Website
# * Status

# %%
def get_attributes(place_id):
    place_details = gmaps.place(
            place_id = place_id,
            fields = [
                "geometry", 
                "opening_hours", 
                "address_component", 
                "formatted_phone_number", 
                "website", 
                "business_status"
            ]
        ).get("result")
    if not place_details:
        return None
    
    # lat / long coords
    coords = place_details.get('geometry').get('location')
    lat = coords.get("lat")
    lng = coords.get("lng")
    if not lat: lat = "No lat listed"
    if not lng: lng = "No lng listed"

    # hours
    hours_list = place_details.get('opening_hours')
    if not hours_list: 
        hours = "No hours listed"
    else:
        hours = '\n'.join(hours_list.get('weekday_text'))

    # zipcode
    address_components = place_details.get('address_components')
    zipcode_details = next(
        (item for item in address_components if 'postal_code' in item['types']), 
        None)
    if not zipcode_details: 
        zipcode = "No zipcode listed"
    else:
        zipcode = zipcode_details.get('long_name')

    # phone number
    phone = place_details.get("formatted_phone_number")
    if not phone: phone = "No phone listed"

    # website
    website = place_details.get("website")
    if not website: website = "No website listed"

    # status
    status = place_details.get("business_status")
    if not status: status = "No status listed"

    return lat, lng, hours, zipcode, phone, website, status


# %%
def lookup_attributes(row):
    place_id = get_place_id(
        row["Store_Name"], 
        row["Address"], 
        row["City"], 
        row["Longitude"], 
        row["Latitude"]
    )
    if not place_id:
        return "No place found", "No place found", "No place found", "No place found", "No place found", "No place found", "No place found"
    lat, lng, hours, zipcode, phone, website, status = get_attributes(place_id)
    return lat, lng, hours, zipcode, phone, website, status

# %% [markdown]
# ## Apply to the entire dataset

# %%
print("Looking up all results")
df["lat_gmaps"], df["lng_gmaps"], df["hours"], df["zip_gmaps"], df["phone"], df["website"], df["status"] = zip(*df.apply(func = lookup_attributes, axis = 1))

# %% [markdown]
# Now let's write this out to a csv to save the results!

# %%
df.to_csv("snap_output_all.csv")
print("Wrote out results.")

import json
import pandas as pd
import os
import glob

#path = 'C:/Users/anjailkatta/GitHub/mega-map-dcl/translations/output'
# filenames = glob.glob(path + '/*.gif')
# for filename in filenames:


os.chdir("/Users/joycetagal/GitHub/dcl-covid-19/mega-map/translations/output")

filenames = glob.glob('./*.json')

for filename in filenames:
    with open(filename, 'r') as data_file:
        data = json.load(data_file)
    #print(data)
    df = pd.DataFrame.from_dict(pd.json_normalize(data))
    for name, values in df.iteritems():
        if values[0] == "":
              del df[name]
        if "\r" in values[0]:
              df[name] = values[0].replace("\r", "")
    df.to_json (filename, orient = "records")



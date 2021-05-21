/*
    This script uses the ADDRESS table data (address_1, city, zip) to call 
    Google Map API and writes the returned latitude and longitude values
    into (new) fields 'newlat' and 'newlong' of the LOCATIONS table.

    It requires a Google API key. To register one of your own, you need to
    create a Google Cloud account. See info here: 
    https://developers.google.com/maps/documentation/javascript/get-api-key.
    Then enable 'Geocoding API' in your account.

    IMPORTANT - paste your Google API key in the field below, replacing the
                placeholder string __YOUR_GOOGLE_API_KEY__. Keep the surrounding
                double quotes.

    There are couple of restrictions to be aware of. Artificial delays of 1s 
    are introduced because of them. 

    1. Google API allows, for 'free' accounts, up to 50 requests per seconds.
       There may be a batch option here too, to send a collection of addresses
       per request. Need to investigate its benefits if available.

    2. Airtable limits update API calls to 15 per second. But each update 
       can have up to 50 records, in batch mode.
*/

const API_KEY = "__YOUR_GOOGLE_API_KEY__";
const GEOCODE_BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json";
const API_LIMIT_PER_SECOND = 50;

//----- helpers ------

let delay = ms => {//setTimeout() doesn't seem to be supported
    let now = new Date();
    now.setMilliseconds(now.getMilliseconds() + ms);
    while (new Date() < now) {;}
};

//one line address to send to API. hard-coded to CA as state
let prepareAddr = (record) => {
    let addr = record.getCellValueAsString('address_1 (from address)') + ','
            +  record.getCellValueAsString('city (from address)') + ',CA,'
            +  record.getCellValueAsString('Zip Code (from address)');

    return addr;
}

let handleResponse = async (succeeded, json, addr) => {
    var newlat = '', newlong = '';

    count++;

    if (!succeeded) {
        error++;
        if (error <= MAX_PRINT_ERROR_COUNT)
            output.text(`ERROR - ${addr}\n\t${json.error_message}`);
    }

    if (count <= MAX_PRINT_COUNT) {
        output.text(`Address: ${addr}`);
        output.inspect(json);
    }

    if (succeeded && json && json.status == 'OK' && json.results) {
        if (json.results.length == 0) {
            incomplete++;
            if (count <= MAX_PRINT_COUNT) {
                output.text('>>>No geocode returned, probably incomplete or invalid address.');
            }
        } else {
            newlat = String(json.results[0].geometry.location.lat);
            newlong = String(json.results[0].geometry.location.lng);
            if (json.results.length > 1) {//not unique, addr is likely ambiguous
                output.text('___ more than one lat/long returned:'+ addr);
            }
            if (count <= MAX_PRINT_COUNT) {
                output.text('>>>latitude='+newlat+'___longitude='+newlong);
            }
        }
    } else {
        if (json.status == 'OVER_QUERY_LIMIT') cnt_api_overage++;
    }

    return [newlat, newlong];
}

//update 50 records in each batch & wait 1 second every 15 batches
//in order to stay within the Airtable limit of "no more than 15 updates per 1000ms"
let batchUpdate = async toUpdate => {
    let cnt_batch = 0;
    while (toUpdate.length > 0) {
        await table.updateRecordsAsync(toUpdate.slice(0,50));
        cnt_batch++;
        if (cnt_batch%15 == 0) delay(1000);
        toUpdate = toUpdate.slice(50);
    }
}

//----- main process -----
output.markdown('# LOCATIONS - populate missing lat/long using Geocoding API');
//track how long it takes to process all records
let start = new Date().getTime();
let MAX_PRINT_COUNT = 5;
let MAX_PRINT_ERROR_COUNT = 10;
output.text(`(only the first ${MAX_PRINT_COUNT} records with missing lat/long will be printed)`);

let table = base.getTable('locations');
let view = table.getView('AutoUpdate latlong');
let allrec = await view.selectRecordsAsync();

let result = allrec.records.filter(rec =>    rec.getCellValueAsString('address') != '' 
                                         &&  rec.getCellValueAsString('address') != 'NA' 
                                         && (rec.getCellValueAsString('city (from address)') != '' ||
                                             rec.getCellValueAsString('Zip Code (from address)') != '') 
                                        //  && (rec.getCellValueAsString('latitude') == '' ||
                                        //      rec.getCellValueAsString('latitude') == 'NA' )
                                   );

let selected = result.length, count = 0, updated=0, error=0, incomplete = 0;

let toUpdate = [], cnt_api = 0, cnt_api_overage = 0;
await Promise.all(
    result.map(async record => {
        let addr = prepareAddr(record);
        
        //google API allows 50 requests per second
        //if exceeed, returned status is OVER_QUERY_LIMIT (json.status) and geocode not returned
        cnt_api++;
        if (cnt_api >= API_LIMIT_PER_SECOND) {
            delay(1005);
            cnt_api = 0;
        }

        let resp = await fetch(GEOCODE_BASE_URL+`?address=${encodeURIComponent(addr)}&key=${API_KEY}`);
        let json = await resp.json();
        let [newlat, newlong] = await handleResponse(resp.ok, json, addr);
        //latitude: -90 to 90 | longitude: -180 to 180

        if (newlat != '' && newlong != '') {
            let newRec = {id: record.id, 
                          fields: {"newlat": Number(newlat), 
                                   "newlong": Number(newlong)
                          }};
            toUpdate.push(newRec);
        } 
    })
);
updated = toUpdate.length;
await batchUpdate(toUpdate);

let end = new Date().getTime(), duration = (end - start) / 1000;
output.markdown('# Done!');
output.text(`${duration} seconds - records selected: ${selected} / updated: ${updated} / incomplete addrs: ${incomplete} / errors: ${error}`);
output.text(`(api rate limited: ${cnt_api_overage})`);


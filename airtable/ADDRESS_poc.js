/*
  This script does a few things using ADDRESS table data:
    - print out a list of unique city names in the 'city' field
    - print out a list of city names in all CAPS
    - identify records whose 'address_1' field contains a city name at the end
    - collect and output some stats related to city or zipcode being missing

  The above information may be helpful for data cleansing efforts.
*/

output.markdown('# Address Table - Unique Cities etc');

//---- helpers ----
let print_stats = (cnt_total, cnt_cityMissing, cnt_zipMissing, cnt_bothMissing, cnt_uniqueCities) => {
    //output.text(`City missing: ${cnt_cityMissing}\tZipcode missing: ${cnt_zipMissing}\tBoth missing: ${cnt_bothMissing}`);
    output.table([
        {Total: `${cnt_total}`,
        CityMissing: `${cnt_cityMissing}`,
        ZipMissing: `${cnt_zipMissing}`,
        BothMissing: `${cnt_bothMissing}`}
    ]);

    output.text('Unique cities: ' + cnt_uniqueCities);    
}

let get_unique_cities = (results) => {
    let cnt_total = results.records.length;
    let cnt_cityMissing = 0, cnt_zipMissing = 0, cnt_bothMissing = 0, 
        cnt_cityParsed = 0;    
    let cities = {}; //unique cities
    let cities_allcaps = {}; //city names in all CAPS

    //get list of cities and stats
    for (let rec of results.records) {
        let cityMissing = false, zipMissing = false;
        let city = rec.getCellValueAsString('city');
        let zip = rec.getCellValueAsString('Zip Code');

        if (city == '' || city == 'NA') {
            cityMissing = true;
            cnt_cityMissing += 1;      
        } else{
            //cities[city.toLowerCase().trim()] = true;
            cities[city] = true;
            //see which city names are in all CAPs
            if (city.trim() === city.trim().toUpperCase())
                cities_allcaps[city] = true;
        }

        if (zip == 'NA' || zip == '') {
            zipMissing = true;
            cnt_zipMissing += 1;
        }
        cnt_bothMissing += cityMissing && zipMissing ? 1 : 0;
    }
    
    print_stats(cnt_total, cnt_cityMissing, cnt_zipMissing, cnt_bothMissing, Object.keys(cities).length);
    return [cities, cities_allcaps];
};

let show_cities = (cities, title) => {
    output.markdown(`### ${title}`);
    let sorted = [], cities_str = '';

    //convert to array in order to sort
    for (var city in cities) 
        sorted.push(city);
    
    sorted = sorted.sort();
    for (var idx in sorted)
        //enclose in double-quotes to preserve ',' in the strings for csv
        cities_str += '"' + sorted[idx] + '"' + '\r\n';

    output.text(cities_str);
}

/* parse address_1 to find city name, iff City field is empty or 'NA'
   input: cities - list of city names already present in City field
          results - records to process
*/
let find_missing_city = (cities, results) => {
    //patterns to search for city name in address_1
    let p_last1 = /.+\s([A-Za-z]+)$/;
    let p_last2 = /.+\s(\w+\s\w+)$/;
    let p_last3 = /.+\s(\w+\s\w+\s\w+)$/;

    //try to parse city name from address_1, usually at the end, 
    //most city names are one or two words. few are three words: East Palo Alto, Half Moon Bay
    let cities_found = {}, cnt_cityFound = 0, cnt_zipEmpty=0;

    for (let rec of results.records) {
        let city = rec.getCellValueAsString('city');
        if (city != '' && city != 'NA') 
            continue;

        let addr = rec.getCellValueAsString('address_1');
        let found = false;

        let matched = addr.match(p_last1); //most cities have 1 word names
        if (matched && matched.length > 1 && cities[matched[1]]) {
                found = true;
        } else {
            matched = addr.match(p_last3); //match last 3 words
            if (matched && matched.length > 1 && cities[matched[1]]) {
                    found = true;
            } else {
                matched = addr.match(p_last2); //match last 2 words
                if (matched && matched.length > 1 && cities[matched[1]]) {
                    found = true;
                }
            }
        } 

        if (found) {
            cnt_cityFound++;
            !cities_found[matched[1]] ? 
                cities_found[matched[1]]=1 : cities_found[matched[1]]++;

            let zip = rec.getCellValueAsString('Zip Code');
            if (zip == '' || zip == 'NA')
                cnt_zipEmpty++;
        }
    }

    return [cities_found, cnt_cityFound, cnt_zipEmpty];
};


//---- main process ----
//select address records - from table directly to get list of unique cities
let table = base.getTable('address');
let results = await table.selectRecordsAsync({fields:['address_1', 'city', 'Zip Code']});
let [cities, cities_allcaps] = get_unique_cities(results);

//select those with missing city values
//let view = table.getView('City is NA');
//results = await view.selectRecordsAsync({fields:['address_1', 'city', 'Zip Code']});

let [cities_found, cnt_cityFound, cnt_zipEmpty] = find_missing_city(cities, results);
output.text(`City Name in address_1: ${cnt_cityFound}\t (zipcode also missing: ${cnt_zipEmpty})`);

show_cities(cities_allcaps, 'City names all in CAPs');
show_cities(cities, 'Unique city names');

/*
Total: 6302 | City missing: 875 | Zipcode missing: 676 | Both missing: 375
Unique cities: 268
City Name in address_1: 293	 (zipcode also missing: 14)
*/


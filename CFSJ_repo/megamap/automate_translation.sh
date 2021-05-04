!/bin/bash\
cd GitHub/mega-map-dcl/translations\
wget --output-file="logs.csv" "https://docs.google.com/spreadsheets/d/17vQZZnKqq4IKXUDjHOsCCLYo0KTxUDsREE7b2Ev4Ang/export?format=csv&gid=1416790411" -O "DCLtranslations.csv"\
 i18n-csv2json-cli --from DCLtranslations.csv --to output --format \
cd output \
rename 's/-.*/.json/' *json\
cd \
cd GitHub/mega-map-dcl/translations\
python modifyJSON.py \


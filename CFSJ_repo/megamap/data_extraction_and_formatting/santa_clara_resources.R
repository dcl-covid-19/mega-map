# Retrieve data behind the Santa Clara County Food Resources map
# Original map: https://csj.maps.arcgis.com/apps/webappviewer/index.html?appid=ddf8ba621416421ebd3fa5ebeeb5e684

# Libraries
library(tidyverse)
library(fs)
library(jsonlite)

# Parameters
  # Map app ID
app_id <- "ddf8ba621416421ebd3fa5ebeeb5e684"
  # Item endpoint
item_endpoint_url <- 
  "https://www.arcgis.com/sharing/rest/content/items/{item_id}/data"
  # API query 
query <- "{url}/query?where=0=0&outFields=*&f=json"
  # Datasets not to read in
datasets_exclude <- 
  c(
    "Santa Clara County Boundary", 
    "Countywide Unincorporated Areas", 
    "Countywide Cities"
  )
  # Directory to write data to
dir_data <- here::here("data")
#===============================================================================

item_endpoint <- function(item_id) {
  str_glue(item_endpoint_url)
}

get_variable <- function(data, variable) {
  data %>% 
    map_chr(variable)
}

arcgis_data <- function(url) {
  data <-
    str_glue(query) %>% 
    read_json()
  
  tibble(location = data$features %>% map("attributes")) %>% 
    unnest_wider(location)
}

webmap_id <-
  jsonlite::read_json(item_endpoint(app_id)) %>% 
  pluck("values", "webmap") 

data <-
  read_json(item_endpoint(webmap_id))$operationalLayers %>% 
  discard(~ .$title %in% datasets_exclude) %>% 
  set_names(
    map_chr(., "title") %>% janitor::make_clean_names()
  ) %>% 
  map_chr("url") %>% 
  map(arcgis_data) %>% 
  walk2(names(.), ~ write_rds(.x, path(dir_data, .y, ext = "rds")))


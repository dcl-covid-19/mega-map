# Engagement data 

# Audience > Behavior > Engagement
# Change date range
# Export > CSV
# Move CSV to data-raw
# Change file_data path so that it points to right data

# Author: Sara Altman
# Version: 2020-11-03

# Libraries
library(tidyverse)

# Parameters
file_data <- 
  here::here(
    "data-raw/Analytics All Web Site Data Engagement 20200601-20201102.csv"
  )
file_out <-
  here::here("data/duration.rds")
#===============================================================================

file_data %>% 
  read_csv(skip = 6) %>% 
  janitor::clean_names() %>% 
  drop_na(contains("session_duration")) %>% 
  rename_with(~ "session_duration", .cols = contains("session_duration")) %>% 
  write_rds(file_out)

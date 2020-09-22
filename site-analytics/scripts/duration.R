# Engagement data 

# Author: Sara Altman
# Version: 2020-08-14

# Libraries
library(tidyverse)

# Parameters
file_data <- 
  here::here(
    "data-raw/Analytics All Web Site Data Engagement 20200601-20200814.csv"
  )
file_out <-
  here::here("data/duration.rds")
#===============================================================================

file_data %>% 
  read_csv(skip = 6) %>% 
  janitor::clean_names() %>% 
  drop_na(session_duration) %>% 
  write_rds(file_out)

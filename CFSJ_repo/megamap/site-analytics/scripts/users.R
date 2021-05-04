# Read in Google Analytics data on users

# To get data:
# Audience > Technology > Browser & OS
# Change the dates to desired date range
# Above the table, select Operating system
# Above the table, select Secondary dimension > Time > Date
# Scroll to the bottom, change the number of rows to be the maximum so that 
  # all rows get exported
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
    "data-raw/Analytics All Web Site Data Browser & OS 20200601-20201102.csv"
  )
file_out <- here::here("data/site_users.rds")
#===============================================================================

v <-
  file_data %>%
  read_csv(
    skip = 6,
    col_types =
      cols(
        `Operating System` = col_character(),
        Date = col_character(),
        Users = col_number(),
        `New Users` = col_number(),
        Sessions = col_number(),
        `Bounce Rate` = col_character(),
        `Pages / Session` = col_double(),
        `Avg. Session Duration` = col_time(),
        `Goal Conversion Rate` = col_character(),
        `Goal Completions` = col_double(),
        `Goal Value` = col_character()
      )
  ) %>%
  janitor::clean_names() %>%
  filter(!is.na(operating_system) & !is.na(users)) %>%
  mutate(
    date = lubridate::ymd(date),
    avg_session_duration = 
      as.double(avg_session_duration) / 60,
    bounce_rate = parse_number(bounce_rate)
  ) %>%
  select(date, everything(), -contains("goal")) %>%
  arrange(date, operating_system) %>%
  write_rds(file_out)

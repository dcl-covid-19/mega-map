# Site event data

# Behavior > Events > Top events
# Select desired date range
# Scroll to table, then click Event label
# Secondary dimension > Users > Operating system
# Select maximum number of rows so that all data shows
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
    "data-raw/Analytics All Web Site Data Top Events 20200601-20201102.csv"
  )
file_out <- here::here("data/events.rds")
#===============================================================================

v <-
  file_data %>% 
  read_csv(
    col_types = 
      cols(
        `Event Label` = col_character(),
        `Operating System` = col_character(),
        `Total Events` = col_number(),
        `Unique Events` = col_number(),
        `Event Value` = col_double(),
        `Avg. Value` = col_double()
      ),
    skip = 6
  ) %>% 
  janitor::clean_names() %>% 
  drop_na(event_label, total_events) %>% 
  separate(col = event_label, into = c("type", "choice"), sep = " - ") %>% 
  mutate(
    type = if_else(str_detect(type, "error"), "error", type),
    choice = str_replace_all(choice, "[-_]", " ")
  ) %>% 
  group_by(type, choice, operating_system) %>% 
  summarize(
    across(c(contains("event"), contains("value")), sum)
  ) %>% 
  ungroup() %>% 
  write_rds(file_out)





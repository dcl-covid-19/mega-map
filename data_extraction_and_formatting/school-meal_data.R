library(tidyverse)
library(googlesheets4)
library(lubridate)

# Parameters

school_meal_key <- "1hAXM1ImpWsQWF12WWY9pMCUKgQBFBmvbR4zm6QhLtws"
school_meal_private <- "1fea1BSSAhbSB0HLsatDaD8wxmwsF7ezQjNvjRK-QJQI"

schools <- 
  read_sheet(
    school_meal_private, 
    col_types = "ccccddicccccccccccDDcccccDDccccc"
  ) 


process_hours <- function(day_of_week, open_hour, close_hour) {
  
  days_long <- c("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
  days_col <- c("mon", "tues", "wed", "thr", "fri", "sat", "sun", "mon", "tues", "wed", "thr", "fri", "sat", "sun")
  
  
  if (is.na(day_of_week)) {
    out <- rep("0", 7)
    names(out) <- days_col[1:7]
    return(out %>% as_tibble_row())
  }
  
  else {
    out <- rep("0", 7)
    
    # for (d in days_of_week) {
    
    t = str_c(open_hour, " - ", close_hour)
    
    # day range
      # All weekdays
    if (str_detect(day_of_week, "Weekdays")) {
      
      for (i in seq(1, 5)) {
        out[i] = t
      }
      # multiple, non contiguous days
    } else if (str_detect(day_of_week, '-')) {
      start = str_split(day_of_week, ' - ') %>% unlist() %>% .[1]
      end = str_split(day_of_week, ' - ') %>% unlist() %>% .[2]
      
      
      if (str_ends(start, 's')) {
        start <- str_sub(start, 1, -2)
      }
      if (str_ends(end, 's')) {
        end <- str_sub(end, 1, -2)
      }
      start_i = match(start, days_long)
      end_i = match(end, days_long[start_i:length(days_long)]) + start_i - 1
      
      for (i in seq(start_i, end_i)) {
        if (i > 7) {
          out[i %% 7] = t
        } else {
          out[i] = t
        }
      }
      # multiple, non contiguous days
    } else if (str_detect(day_of_week, "through")) {
      
      start = str_split(day_of_week, ' through ') %>% unlist() %>% .[1]
      end = str_split(day_of_week, ' through ') %>% unlist() %>% .[2]
      
      
      if (str_ends(start, 's')) {
        start <- str_sub(start, 1, -2)
      }
      if (str_ends(end, 's')) {
        end <- str_sub(end, 1, -2)
      }
      start_i = match(start, days_long)
      end_i = match(end, days_long[start_i:length(days_long)]) + start_i - 1
      
      for (i in seq(start_i, end_i)) {
        if (i > 7) {
          out[i %% 7] = t
        } else {
          out[i] = t
        }
      }
      
    }
    
    else if (str_detect(day_of_week, ', ')) {
      for (single_d in str_split(day_of_week, ', ') %>% unlist()) {
        if (str_ends(single_d, 's')) {
          single_d <- str_sub(single_d, 1, -2)
        }
        start_i = match(single_d, days_long)
        out[start_i] = t
      }
      # single day
    } else {
      if (str_ends(day_of_week, 's')) {
        day_of_week <- str_sub(d, 1, -2)
      }
      start_i = match(day_of_week, days_long)
      
      if (is.na(start_i)) {
        stop()
      }
      out[start_i] = t
    }
    
    
    out <- str_to_upper(out)
    names(out) <- days_col[1:7]
    return(out %>% as_tibble_row())
    
  }
  
  out <- rep(days_of_week, 7)
  names(out) <- days_col[1:7]
  return(out %>% as_tibble_row())
  
}


days <- schools$days_of_week[1:20]
opens <- schools$open_hour[1:20]
closes <- schools$close_hour[1:20]

outdf <- pmap_dfr(list(days, opens, closes), process_hours)

mapped_schools <- 
  pmap_dfr(
    .l = list(schools$days_of_week, schools$open_hour, schools$close_hour), 
    .f = process_hours
  )


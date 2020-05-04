key <- '11tdkyX0kR8nRwMUktohdp2Wx1fGiMiHrlUP4i_8ctPM'
com_resources <- 
  read_sheet(key, col_types = "ccccccddcccdccccccccccDccccc") %>%
  filter(!is.na(Type), str_detect(Type, "Groceries|Meal"), status == "Open")

process_hours <- function(day_hour, senior = FALSE) {
  
  days_long <- c("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
  days_col_normal <- c("mon", "tues", "wed", "thr", "fri", "sat", "sun", "mon", "tues", "wed", "thr", "fri", "sat", "sun")
  days_col_senior <- str_c("sp_", days_col_normal)
  
  if (senior) {
    days_col <- days_col_senior
  } else {
    days_col <- days_col_normal
  }
  
  
  if (is.na(day_hour)) {
    out <- rep("0", 7)
    names(out) <- days_col[1:7]
    return(out %>% as_tibble_row())
  }
  
  else if (str_detect(day_hour, ';')) {
    out <- rep("0", 7)
    
    for (dt in str_split(day_hour, ';') %>% unlist()) { # change \\n to ;
      
      d <-  str_split(dt, ': ') %>% unlist() %>% .[1] 
      if (str_detect(d, "^[0-9]")) {
        w <- str_split(d, " ") %>% unlist() %>% .[1] %>% str_extract(., "[0-9]{1}")
        d <- str_split(d, " ") %>% unlist() %>% .[2]
      }
      t <- str_split(dt, ': ') %>% unlist() %>% .[2]
      
      # day range
      if (str_detect(d, '-')) {
        start = str_split(d, ' - ') %>% unlist() %>% .[1]
        end = str_split(d, ' - ') %>% unlist() %>% .[2]
        
        
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
      } else if (str_detect(d, ', ')) {
        for (single_d in str_split(d, ', ') %>% unlist()) {
          if (str_ends(single_d, 's')) {
            single_d <- str_sub(single_d, 1, -2)
          }
          start_i = match(single_d, days_long)
          out[start_i] = t
        }
        # single day
      } else {
        if (str_ends(d, 's')) {
          d <- str_sub(d, 1, -2)
        }
        start_i = match(d, days_long)
        
        if (is.na(start_i)) {
          stop()
        }
        out[start_i] = t
      }
    }
    
    out <- str_to_upper(out)
    names(out) <- days_col[1:7]
    return(out %>% as_tibble_row())
    
  }
  
  else {
    out <- rep("0", 7)
    
    for (dt in str_split(day_hour, ';') %>% unlist()) { # change \\n to ;
      
      d <-  str_split(dt, ': ') %>% unlist() %>% .[1] 
      if (str_detect(d, "^[0-9]")) {
        w <- str_split(d, " ") %>% unlist() %>% .[1] %>% str_extract(., "[0-9]{1}")
        d <- str_split(d, " ") %>% unlist() %>% .[2]
      }
      t <- str_split(dt, ': ') %>% unlist() %>% .[2]
      
      # day range
      if (str_detect(d, '-')) {
        start = str_split(d, ' - ') %>% unlist() %>% .[1]
        end = str_split(d, ' - ') %>% unlist() %>% .[2]
        
        
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
      } else if (str_detect(d, ', ')) {
        for (single_d in str_split(d, ', ') %>% unlist()) {
          if (str_ends(single_d, 's')) {
            single_d <- str_sub(single_d, 1, -2)
          }
          start_i = match(single_d, days_long)
          out[start_i] = t
        }
        # single day
      } else {
        if (str_ends(d, 's')) {
          d <- str_sub(d, 1, -2)
        }
        start_i = match(d, days_long)
        
        if (is.na(start_i)) {
          stop()
        }
        out[start_i] = t
      }
    }
    
    out <- str_to_upper(out)
    names(out) <- days_col[1:7]
    return(out %>% as_tibble_row())
    
  }
  
  out <- rep(day_hour, 7)
  names(out) <- days_col[1:7]
  return(out %>% as_tibble_row())
  
}



## Test process_hours

days_hours_test <- com_resources$days_hours[5]
process_hours(days_hours_test)

process_hours(com_resources$days_hours)



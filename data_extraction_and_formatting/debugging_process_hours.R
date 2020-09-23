
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
    out <- rep("0", 8)
    names(out) <- c(days_col[1:7], "additional_hours")
    return(out %>% as_tibble_row())
  }
  
  try({
    out <- rep("0", 8)
    
    # split into groups of "days: hours"
    for (dt in str_split(day_hour, '[\\n;,]+') %>% unlist()) {
      dt <- str_trim(dt)
      d <-  str_split(dt, ': ') %>% unlist() %>% .[1]
      t <- str_split(dt, ': ') %>% unlist() %>% .[2]
      
      # handles additional openings on odd days
      if (str_starts(str_trim(d, side = "left"), "\\d+")) {
        out[8] <- if (out[8] == "0") dt else str_c(out[8], dt, sep = ", ")
        next
      }
      
      # handles normal opening hours
      # day range
      if (str_detect(d, '-')) {
        start = str_split(d, ' - ') %>% unlist() %>% .[1]
        end = str_split(d, ' - ') %>% unlist() %>% .[2]
        
        # remove plurals
        if (str_ends(start, 's')) {
          start <- str_sub(start, 1, -2)
        }
        if (str_ends(end, 's')) {
          end <- str_sub(end, 1, -2)
        }
        
        # find corresponding day indeces
        start_i = match(start, days_long)
        end_i = match(end, days_long[start_i : length(days_long)]) + start_i - 1
        
        # populate output vector
        for (i in seq(start_i, end_i)) {
          if (i > 7) {
            out[i %% 7] = if (out[i %% 7] == "0") t else str_c(out[i %% 7], t, sep = ", ")
          } else {
            out[i] = if (out[i] == "0") t else str_c(out[i], t, sep = ", ")
          }
        }
        # multiple, non contiguous days
      } else if (str_detect(d, ', ')) {
        
        # split by days, find index and populate output
        for (single_d in str_split(d, ', ') %>% unlist()) {
          if (str_ends(single_d, 's')) {
            single_d <- str_sub(single_d, 1, -2)
          }
          start_i = match(single_d, days_long)
          out[start_i] = if (out[start_i] == "0") t else str_c(out[start_i], t, sep = ", ")
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
        out[start_i] = if (out[start_i] == "0") t else str_c(out[start_i], t, sep = ", ")
      }
    }
    
    out <- str_to_upper(out) %>% replace_na("")
    names(out) <- c(days_col[1:7], "additional_hours")
    return(out %>% as_tibble_row())
    
  }, silent = T)
  
  # handles unparsable text
  out <- c(rep(day_hour, 7), "0")
  names(out) <- c(days_col[1:7], "additional_hours")
  return(out %>% as_tibble_row())
  
}

comm_resource_data %>% tail(10)
comm_resource_data$days_hours %>% head(10)

comm_resource_data$days_hours %>% head(10) %>%
  map_dfr(process_hours)

str_split(day_hour, "[\\n,;]") 
dt <- "Mon - Thurs: 9:00am - 8:00pm"

dt <- "Monday, Wednesday, Friday: 9:00am - 8:00pm"
process_hours(dt)

dt <- str_trim(dt)
d <-  str_split(dt, ': ') %>% unlist() %>% .[1]
t <- str_split(dt, ': ') %>% unlist() %>% .[2]

day_hour <- "Mon - Thurs: 9:00am - 8:00pm, Friday: 9:00am - 4:00pm, Saturday : 10:00am - 2:00pm"

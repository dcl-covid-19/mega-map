Bay Area Community Analytics
================
Sara Altman
2020-08-14

  - [Users over time](#users-over-time)
  - [Operating systems](#operating-systems)
  - [Time spent on the site](#time-spent-on-the-site)

``` r
# Libraries
library(tidyverse)
library(lubridate)

# Parameters
file_users <- here::here("data/site_users.rds")
file_duration <- here::here("data/duration.rds")
#===============================================================================

users <-
  file_users %>% 
  read_rds()

duration <-
  file_duration %>% 
  read_rds()
```

## Users over time

``` r
users %>% 
  count(date, wt = users) %>% 
  ggplot(aes(date, n)) +
  geom_point() +
  geom_line() +
  scale_x_date(
    date_labels = "%b %d", 
    breaks = 
      c(
        unique(floor_date(users$date, unit = "month")), 
        unique(floor_date(users$date, unit = "month")) + 14
      )
  ) +
  scale_y_continuous(breaks = scales::breaks_width(10)) +
  labs(
    x = "Date",
    y = "Number of users"
  )
```

![](analytics_files/figure-gfm/unnamed-chunk-2-1.png)<!-- -->

``` r
users %>% 
  group_by(week = floor_date(date, unit = "week")) %>%
  summarize(new_users = sum(new_users) / sum(users)) %>%
  ggplot(aes(week, new_users)) +
  geom_line() +
  geom_point() +
  scale_y_continuous(
    limits = c(0, 1), 
    labels = scales::label_percent()
  ) +
  labs(
    x = "Week",
    y = "Percent new users"
  )
```

    ## `summarise()` ungrouping output (override with `.groups` argument)

![](analytics_files/figure-gfm/unnamed-chunk-3-1.png)<!-- -->

## Operating systems

``` r
users %>% 
  count(operating_system, wt = users) %>% 
  mutate(
    percent = n / sum(n),
    operating_system = fct_reorder(operating_system, n, .desc = TRUE)
  ) %>% 
  ggplot(aes(operating_system, percent)) +
  geom_col() +
  scale_y_continuous(
    labels = scales::label_percent(accuracy = 1), 
    breaks = scales::breaks_width(0.1)
  ) +
  labs(
    x = "Operating system",
    y = "Percent of users",
    title = "Users by operating system",
    subtitle = "Most use Mac or iOS"
  )
```

![](analytics_files/figure-gfm/unnamed-chunk-4-1.png)<!-- -->

## Time spent on the site

``` r
duration %>% 
  mutate(
    percentage = sessions/sum(sessions),
    duration_min = 
      as.double(str_extract(session_duration, "^\\d+")),
    session_duration = 
      str_remove(session_duration, " seconds") %>% 
      fct_reorder(duration_min) 
  ) %>% 
  ggplot(aes(session_duration, percentage)) +
  geom_col() +
  scale_y_continuous(
    labels = scales::label_percent(accuracy = 1),
    breaks = scales::breaks_width(width = 0.1)
  ) +
  labs(
    x = "Session duration (seconds)",
    y = "Percentage of sessions",
    title = "Session duration"
  )
```

![](analytics_files/figure-gfm/unnamed-chunk-5-1.png)<!-- -->

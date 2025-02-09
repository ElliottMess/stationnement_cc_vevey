library(dplyr)
library(glue)
library(rvest)
library(readr)

get_video_description <- function(url){
    page <- read_html(url)
    page %>%
        html_elements("#description-inline-expander")
}

video_conseils <- readr::read_csv("data/youtube_videos_cc.csv", show_col_types = FALSE) %>%
    mutate( url = glue::glue("https://www.youtube.com/watch?v={video_id}"))


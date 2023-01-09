library(tidyverse)
library(purrr)
library(useful)
library(data.table)
full777 <- read_csv("full777.csv")


#intolist <- function(rel){
as.list(strsplit(substring(rel, 3, nchar(rel) - 2), "), (", fixed = TRUE)[[1]])
}

compare_list <- function(rel1, rel2){
  s.a <- strsplit(rel1, "")[[1]]
  s.b <- strsplit(rel2, "")[[1]]
  paste(s.a[s.a != s.b], collapse = "")
}


fullplays_edit <- full777 %>%
  unite("gameplayId", gameId, playId) %>%
  mutate(stunt_code = str_replace_all(relative_location_list, c("[[:punct:]]" = "", " " = "", "0" = ""))) %>%
  mutate(relative_location_list = str_replace_all(relative_location_list, c("0.0, " = ""))) %>%
  # mutate(relative_location_list = map(relative_location_list, intolist)) %>%
  # first condition put in because of errors with relative locations - weird stuff going on sometimes
  mutate(stunt = ifelse(nchar(stunt_code) != nchar(lag(stunt_code)) | gameplayId != lag(gameplayId) | stunt_code == lag(stunt_code), 0, 1))


just_stunts <- fullplays_edit %>%
  filter(stunt == 1 | lead(stunt) == 1) %>%
  mutate(diff = NA)


for (i in seq(2, nrow(just_stunts), 2)){
  just_stunts$diff[i] = compare_list(just_stunts$stunt_code[i], just_stunts$stunt_code[i-1])
}


new_full_plays <- fullplays_edit %>%
  left_join(just_stunts[c(1,11)], by = "...1") %>%
  mutate(player_loc = relative_location)


for (i in 1:nrow(new_full_plays)){
  if(new_full_plays$stunt[i] == 1 & !is.na(new_full_plays$diff[i])){
    for (j in 1:(nchar(new_full_plays$stunt_code[i]) - 1)){
      new_full_plays$diff[i+j] = new_full_plays$diff[i]
    }
  }
}


# for the lists with a bunch of 0s at the beginning
i <- 1
while (i <= nrow(new_full_plays)){
  if (new_full_plays$relative_location[i] == 0){
    for (j in 1:nchar(new_full_plays$stunt_code[i])){
      new_full_plays$player_loc[i] = substring(new_full_plays$stunt_code[i], j, j)
      i = i + 1
    }
    i = i - 1
  }
  i = i + 1
}


front <- new_full_plays %>%
  mutate(x_coord = ifelse(mapply(grepl, player_loc, diff), x, NA)) %>%
  filter(!is.na(diff)) %>%
  mutate(diff = map(diff, function(x) (paste(sort(unlist(strsplit(x, ""))), collapse = "")))) %>%
  mutate(diff1 = ifelse(nchar(diff) >= 4, substring(diff, 1, 2), NA)) %>%
  mutate(diff2 = ifelse(nchar(diff) >= 4, substring(diff, 3, 4), NA)) %>%
  mutate(x_coord1 = ifelse(mapply(grepl, player_loc, diff1), x, NA)) %>%
  mutate(x_coord2 = ifelse(mapply(grepl, player_loc, diff2), x, NA)) %>%
  group_by(gameplayId, time) %>%
  mutate(front = ifelse(nchar(diff) <= 3, ifelse(playDirection == 'right', min(x_coord, na.rm = TRUE), max(x_coord, na.rm = TRUE)), NA)) %>%
  mutate(back = ifelse(nchar(diff) <= 3, ifelse(playDirection == 'right', max(x_coord, na.rm = TRUE), min(x_coord, na.rm = TRUE)), NA)) %>%
  mutate(front1 = ifelse(!is.na(diff1), ifelse(playDirection == 'right', min(x_coord1, na.rm = TRUE), max(x_coord1, na.rm = TRUE)), NA)) %>%
  mutate(front2 = ifelse(nchar(diff2) <= 3, ifelse(playDirection == 'right', min(x_coord2, na.rm = TRUE), max(x_coord2, na.rm = TRUE)), NA)) %>%
  mutate(back1 = ifelse(nchar(diff1) <= 3, ifelse(playDirection == 'right', max(x_coord1, na.rm = TRUE), min(x_coord1, na.rm = TRUE)), NA)) %>%
  mutate(back2 = ifelse(nchar(diff2) <= 3, ifelse(playDirection == 'right', max(x_coord2, na.rm = TRUE), min(x_coord2, na.rm = TRUE)), NA)) %>%
  mutate(front_back = ifelse(front == x_coord, 'front', ifelse(back == x_coord, 'back', NA))) %>%
  mutate(front_back = ifelse(nchar(diff) >= 4, ifelse(front1 == x_coord | front2 == x_coord, 'front', ifelse(back1 == x_coord | back2 == x_coord, 'back', NA)), front_back)) %>%
  filter('front' %in% front_back & 'back' %in% front_back) %>%
  mutate(who_front = ifelse(front_back == 'front', player_loc, NA)) %>%
  mutate(who_back = ifelse(front_back == 'back', player_loc, NA)) %>%
  mutate(all_front = list(who_front[!is.na(who_front)])) %>%
  mutate(all_back = list(who_back[!is.na(who_back)])) 





final <- left_join(new_full_plays, front[c(1,13:28)], by = c('...1')) %>%
  select(c(1:4, 7:8, 10, 24, 27:28)) %>%
  group_by(gameplayId, time) %>%
  mutate(stunt = ifelse(sum(front_back == 'front', na.rm = TRUE) == 2, 2, ifelse(1 %in% stunt, 1, 0))) %>%
  filter(stunt > 0) %>%
  mutate(first = { stunt >= 1 } %>% { . * !duplicated(.) } ) %>%
  filter(first == 1 & !(list(NULL) %in% all_front)) %>%
  select(-c(8, 11)) %>%
  separate(gameplayId, c('gameId', 'playId'), sep = "_")


final$all_front = as.character(final$all_front)
final$all_back = as.character(final$all_back)


write.csv(final, "full_front_back_data.csv")


# gets messed up with the zeros (11307, 55041)
# fixed

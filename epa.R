library(tidyverse)
addepa <- read_csv("addepa.csv")
finalplays <- read_csv("finalplays.csv")

addepa$gameId <- as.character(addepa$gameId)

epa <- addepa %>%
  inner_join(nflreadr::load_pbp(2021) %>%
               select(play_id, old_game_id, epa), 
             by=c("playId"="play_id","gameId"="old_game_id"))

epa$gameId <- as.numeric(epa$gameId)

View(epa)

with_epa <- epa %>%
  mutate(`('stunt_class', '')` = ifelse(`('stunt_class', '')` %in% c(7,8,11,12), 13, `('stunt_class', '')`)) %>%
  mutate(`('blitz_class', '')` = ifelse(`('blitz_class', '')` %in% c(6,8), 10, `('blitz_class', '')`))         


write.csv(with_epa, "with_epa.csv")



finalplays$gameId <- as.character(finalplays$gameId)
finalplays$playId <- as.character(finalplays$playId)

change <- left_join(finalplays, front[c(2,3,6)], by = c("gameId", "playId"))
change2 <- unique(change)



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

change3 <- filter(change2, ((`('stunt_class', '')` == 2) & (pff_playAction == 0) & (`('blitz_class', '')` %in% (c(0,2,3)))) | ((`('stunt_class', '')` == 4) & (pff_playAction == 0) & (`('blitz_class', '')` == 0)))

change3$gameId <- as.numeric(change3$gameId)
change3$playId <- as.numeric(change3$playId)

change4 <- left_join(change3, with_epa[c(2,3,38)], by = c("gameId", "playId"))

change5 <- filter(change4, `('stunt_class', '').y` == 0)


for (i in 1:nrow(change5)){
  if (change5$playDirection[i] == 'left'){
    if (change5$`('stunt_class', '').x`[i] == 2){
      change5$`('stunt_class', '').x`[i] = 4
    }
    else{
      change5$`('stunt_class', '').x`[i] = 2
    }
  }
  i = i + 1
}

with_epa2 <- left_join(with_epa, change5[c(2,3,37)], by = c("gameId", "playId"))

with_epa2 <- mutate(with_epa2, `('stunt_class', '')` = ifelse(!is.na(`('stunt_class', '').x`), `('stunt_class', '').x`, `('stunt_class', '')`))
with_epa2 <- select(with_epa2, -c(41))

with_epa <- with_epa2



write.csv(with_epa, "with_epa.csv")

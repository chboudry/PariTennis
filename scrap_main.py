from scrap_atp_tournaments import *
from scrap_atp_match_scores import *
from scrap_atp_match_stats import *
from scrap_atp_players import *

# # # # # # # # # # #
#                   #
#   MAIN ROUTINE    #
#                   #
# # # # # # # # # # #

# generate scrapped files
# Warning : this takes extensive time, up to 24h for match stats files from 2000 to 2023
#generate_tournaments(2000, 2023, "./data/tournaments.csv")
#generate_matchs(2000, 2023, "./data/matchs.csv")
#generate_match_stats("./data/2023-matchs.csv","./data/2023-matchs-stats.csv", "./data/2023-matchs-stats-advanced.csv")
#generate_players("./data/matchs.csv", "./data/players.csv")
from tournaments import *
from match_scores import *
from match_stats import *

# # # # # # # # # # #
#                   #
#   MAIN ROUTINE    #
#                   #
# # # # # # # # # # #

# generate ATP files
# Warning : this takes extensive time, up to 24h for match stats files from 2000 to 2023
#generate_tournaments(2000, 2023, "./data/tournaments.csv")
#generate_matchs(2000, 2023, "./data/matchs.csv")
generate_match_stats("./data/2023-matchs.csv","./data/2023-matchs-stats.csv", "./data/2023-matchs-stats-advanced.csv")
#generate_players_overview("./data/matchs.csv", "./data/players.csv")
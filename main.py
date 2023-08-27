from tournaments import *
from match_scores import *
from match_stats import *

# # # # # # # # # # #
#                   #
#   MAIN ROUTINE    #
#                   #
# # # # # # # # # # #

# generate tournaments file
#generate_tournaments(2000, 2023, "./data/tournaments.csv")

# generate matchs scores files
#generate_matchs(2000, 2023, "./data/matchs.csv")

# generate matchs stats files
generate_match_stats("./data/matchs.csv","./data/matchs-stats.csv", "./data/matchs-stats-advanced.csv")
from scrap_couk_data import *
from generate_players_file import *
from generate_tournaments_file import *
from generate_training_dataset import *
from shuffle_training_dataset import *

################################################################################
########################## Building dataset ####################################
################################################################################

# if they are not already there, downlaod xls files into data folder
# they can be pick up from http://tennis-data.co.uk/alldata.php
# this is a manual step 


# the following function automatically pick the excel files in /data, no parameter for this is required
# concat rows and save result in provided file path
# does not modify any raw data
# do create the elo columns, which may be removed
generate_atp_data("./data/atp_data.csv")


# generating players base using X to Y data, X, Y included
# this will be static data whatever the match studied
# execute only once each time you change the date parameters
generate_player_global_file("./data/atp_data.csv", 2004, 2023, "./data/players.csv")

# generating tournaments base 
# this will be static data 
# execute only once each time you update the atp_data.csv
# this is only used when getting fresh y from the web, because we can't scrap all of the tournament settings
generate_tournaments_file("./data/atp_data.csv", "./data/tournaments.csv")


# building of the training dataset
# provide start year and end year included
generate_training_dataset("./data/atp_data.csv", "./data/players.csv", 2019, 2023, "./data/training_dataset.csv")


# shuffle
# right now, player 1 is always the winner, we need to shuffle the data a bit to avoid that
# shuffle algorithm is we pick 5 row random out of 10 and make player 2 the winner (= switching player 1 and player 2 info and resetting player_winner1 accordingly)
shuffle_training_dataset("./data/training_dataset.csv", "./data/training_dataset.csv")


# play with a model within a notebook 
# use your last training dataset to train the model
# note : players fucntion is updated frequently, 
# make sure your model PICK the columns you want to work on, and NOT DROP the one you don't want
# because if you choose to drop, next time players database is updated, il will break your code
# Some model examples are :
# m1_decisiontree.ipynb
# m2c_gradientboosting.ipynb


# to generate prod data for prediction 
# use the generate_y_real function within your notebook
# 1. execute to populate most of the rows in a file
## from generate_x_prod import *
## atpurl = "https://www.atptour.com/en/scores/current/us-open/560/daily-schedule"
## playersfile="./data/players.csv"
## tournamentsfile="./data/tournaments.csv"
## outputfile ="./data/y_topredict.csv"
## generate_x_prod(playersfile, tournamentsfile, atpurl, outputfile)
# 2. edit to add odds per match
# 3. apply any transformation suited to X for you model needs
# 4. run your model prediction


import pandas as pd
import numpy as np
import datetime
import math


from generate_player_global_file import *
from generate_training_dataset import *

################################################################################
########################## Building dataset ####################################
################################################################################

# generating players base using 2004 to 2020 data
# This will be static data whatever the match studied
# Execute only once each time you change the date parameters
# generate_player_global_file("./data/atp_data.csv", 2004, 2020, "./data/players.csv")

## building of the training dataset
generate_training_dataset("./data/atp_data.csv", "./data/players.csv", 2021, 2023, "./data/training_dataset.csv")

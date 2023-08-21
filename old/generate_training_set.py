from datetime import datetime,timedelta

from old.past_features import *
#from elo_features import *
from old.categorical_features import *
from old.strategy_assessment import *
from old.utilities import *


################################################################################
######################## Building training set #################################
################################################################################
### We'll add some features to the dataset

data=pd.read_csv("./Data/atp_data.csv")
data.Date = data.Date.apply(lambda x:datetime.datetime.strptime(x, '%Y-%m-%d'))


######################### The period that interests us #########################

beg = datetime.datetime(2008,1,1) 
end = data.Date.iloc[-1]
indices = data[(data.Date>beg)&(data.Date<=end)].index

################### Building of some features based on the past ################

features_player  = features_past_generation(features_player_creation,5,"playerft5",data,indices)
features_duo     = features_past_generation(features_duo_creation,150,"duoft",data,indices)
features_general = features_past_generation(features_general_creation,150,"generalft",data,indices)
features_recent  = features_past_generation(features_recent_creation,150,"recentft",data,indices)
#dump(player_features,"player_features")
#dump(duo_features,"duo_features")
#dump(general_features,"general_features")
#dump(recent_features,"recent_features")
#features_player=load("player_features")
#features_duo=load("duo_features")
#features_general=load("general_features")
#features_recent=load("recent_features")

########################### Selection of our period ############################

data = data.iloc[indices,:].reset_index(drop=True)
odds = data[["PSW","PSL"]]

########################## Encoding of categorical features ####################

features_categorical = data[["Series","Court","Surface","Round","Best of","Tournament"]]
features_categorical_encoded = categorical_features_encoding(features_categorical)
players_encoded = features_players_encoding(data)
tournaments_encoded = features_tournaments_encoding(data)
features_onehot = pd.concat([features_categorical_encoded,players_encoded,tournaments_encoded],axis=1)


############################### Duplication of rows ############################
## For the moment we have one row per match. 
## We "duplicate" each row to have one row for each outcome of each match. 
## Of course it isn't a simple duplication of  each row, we need to "invert" some features

# Elo data
elo_rankings = data[["elo_winner","elo_loser","proba_elo"]]
elo_1 = elo_rankings
elo_2 = elo_1[["elo_loser","elo_winner","proba_elo"]]
elo_2.columns = ["elo_winner","elo_loser","proba_elo"]
elo_2.proba_elo = 1-elo_2.proba_elo
elo_2.index = range(1,2*len(elo_1),2)
elo_1.index = range(0,2*len(elo_1),2)
features_elo_ranking = pd.concat([elo_1,elo_2]).sort_index(kind='merge')

# Categorical features
features_onehot = pd.DataFrame(np.repeat(features_onehot.values,2, axis=0),columns=features_onehot.columns)

# odds feature
features_odds = pd.Series(odds.values.flatten(),name="odds")
features_odds = pd.DataFrame(features_odds)

### Building of the final dataset
# You can remove some features to see the effect on the ROI
features = pd.concat([features_odds,
                  features_elo_ranking,
                  features_onehot,
                  features_player,
                  features_duo,
                  features_general,
                  features_recent],axis=1)

features.to_csv("./Data/atp_data_features.csv",index=False)

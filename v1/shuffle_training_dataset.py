import pandas as pd
import random

## funtion to rotate player 1 and player 2 without knowing columns names
## requires player columns to be called playerX_ to work
def shuffle_training_dataset(data_in, data_out):
    # loading data in memory
    data=pd.read_csv(data_in)
    rowindex = random.sample(range(0, data.shape[0]-1), ((data.shape[0]-1)//2))

    cols=[]

    for col in data.columns:
        if (col.startswith("player1_")):
            cols.append(col[8:])

    for index in rowindex:
        for col in cols :
            player1_col = "player1_" + col
            player2_col = "player2_" + col
            temp = data.iloc[index][player1_col]
            data.at[data.index[index],player1_col] = data.at[data.index[index],player2_col]
            data.at[data.index[index],player2_col] = temp
        data.at[data.index[index],"winner_player1"] = 0

        temp = data.at[data.index[index],"match_odd_player1"]
        data.at[data.index[index],"match_odd_player1"] = data.at[data.index[index],"match_odd_player2"]
        data.at[data.index[index],"match_odd_player2"] = temp

    data.to_csv(data_out,index=False)
import datetime
import pandas as pd

# If we execute : 
# df = pd.read_csv("./data/atp_data.csv")
# temp = (df.loc[:,["Tournament","Series","Court","Surface","Round"]]).groupby(by="Tournament").nunique()
# temp.loc[temp.Series>1]
# temp.loc[temp.Court>1]
# temp.loc[temp.surface>1]
# We can see that they are actually quite some change of tournament settings
# We already have the setting per match thanks to atp dataset
# So this script will generate tournament setting based on last tournament setting played
# Note, the change are usually documented in Wikipedia 
# aka : The Antalya Open is an ATP Tour 250 series tennis tournament on the ATP Tour launched in June 2017 in Antalya, Turkey.
# [1] The tournament was played on grass courts until 2019.
# [2] In 2021 it was played on hard courts.[3]


def generate_tournaments_file(atp_data_file, tournament_file):
    # loading data in memory
    df = pd.read_csv(atp_data_file)

    tournaments = df.loc[:,["Tournament"]].drop_duplicates()

    # building tournament dataset
    tournaments_name = []
    tournaments_serie = []
    tournaments_location = []
    tournaments_court = []
    tournaments_surface = []
    tournaments_totalrounds = []
    tournaments_bestof = []

    for tournament in tournaments.values.tolist():
            tournament = tournament[0]
            tournamentmatchs = df.loc[df.Tournament==tournament].copy()
            tournamentmatchs.Date = tournamentmatchs.Date.apply(lambda x:datetime.datetime.strptime(x, '%Y-%m-%d'))
            tournamentmatchs["years"] = tournamentmatchs.Date.apply(lambda x:x.year)
            lastyeartournament = tournamentmatchs["years"].max()
            tournamentmatchs = tournamentmatchs.loc[tournamentmatchs.years==lastyeartournament].copy()

            tournaments_name.append(tournamentmatchs["Tournament"].iloc[0])
            tournaments_serie.append(tournamentmatchs["Series"].iloc[0])
            tournaments_location.append(tournamentmatchs["Location"].iloc[0])
            tournaments_court.append(tournamentmatchs["Court"].iloc[0])
            tournaments_surface.append(tournamentmatchs["Surface"].iloc[0])
            tournaments_bestof.append(tournamentmatchs["Best of"].iloc[0])

            tournaments_totalrounds.append(tournamentmatchs.loc[:,["Round"]].drop_duplicates().count()[0])

    d = {
        'name': tournaments_name, 
        'serie':tournaments_serie,
        'location': tournaments_location, 
        'court':tournaments_court, 
        'surface':tournaments_surface,
        'totalrounds':tournaments_totalrounds,
        'bestof': tournaments_bestof}

    df_tournaments = pd.DataFrame(data=d)
    df_tournaments.to_csv(tournament_file,index=False)
# Pari Tennis

Machine learning on Tennis Bets !

## How to use

### Startup
- create a fresh virtual environment : py -m venv env
- on visual studio code you might have to elevate your prompt : Set-ExecutionPolicy Unrestricted -Scope Process
- activate your environment : .\env\Scripts\activate
- active your virtual environment : py -m pip install -r requirements.txt

### Scrapping data

- This is optional and not recommended (very long) as all datas are already scrapped and in folder
- Data is coming from multiples sources :
  - https://www.atptour.com for tournaments, matchs, matchs stats and players
  - http://tennis-data.co.uk/alldata.php for matchs odds and players ranking in time

### Formatting data 

What generate_training_dataset does :
1. Merge scrapped atp match data + scrapped atp players data + scrapped tennis-data.co.uk alltogeter per match
2. winner player is rename as player 1, loser player is rename as player 2
3. 50% of the data are randomly schuffled (inverting player 1 and player 2) so that winner may be 1 or 2

### Todo

scrapping :
- get odds

Get players : 
- performance per tournament (habits to go in finals)
- progression over last X month / last X tournaments
- timeplay regularity
- overall performance over higher ranking
- overall performance over below ranking
- did this tournament already (yes :1 : no : 0)
- lefty / righty
- intéger la fréquence moyenne de blessures annuelles dans le roi (le ROI peut il absorber cette perte ?)

Get next tournaments:
- create a predict function that only use a date parameter to get the next match on the internet

## Source

Code in V1 was initally a fork from : https://github.com/edouardthom/ATPBetting
Code in V2 is using scrapping code from : https://github.com/serve-and-volley/atp-world-tour-tennis-data 
# Pari Tennis

Machine learning on Tennis Bets !

## How to use

### Startup
- create a fresh virtual environment : py -m venv env
- on visual studio code you might have to elevate your prompt : Set-ExecutionPolicy Unrestricted -Scope Process
- activate your environment : .\env\Scripts\activate
- active your virtual environment : py -m pip install -r requirements.txt

### Refresh data

- download xls files from http://tennis-data.co.uk/alldata.php in the data directory
- in the env terminal, execute : python ./generate_atp_data.py
- this will generate the atp_data.csv file

### Generate a new training dataset 

- in the env terminal, execute : python .\generate_dataset_file.py
- this will generate training_dataset.csv file

### Todo

scrapping :
- fix a2018 function for empty url
- generate players
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
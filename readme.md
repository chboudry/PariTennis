# Pari Tennis

Machine learning on Tennis Bets !

### How to use
- create a fresh virtual environment : py -m venv env
- on visual studio code you might have to elevate your prompt : Set-ExecutionPolicy Unrestricted -Scope Process
- activate your environment : .\env\Scripts\activate
- active your virtual environment : py -m pip install -r requirements.txt

#### Refresh data

- in the env terminal, execute : python ./generate_atp_data.py


### Generate 

- To generate atp_data_features.csv, in the env terminal, execute : python .\generate_training_set.py

### Source

https://github.com/edouardthom/ATPBetting
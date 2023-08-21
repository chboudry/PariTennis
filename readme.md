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

## Source

https://github.com/edouardthom/ATPBetting
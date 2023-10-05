"""

Config file for Streamlit App

Note: typo convension: global variables are uppercase

"""

from member import Member


TITLE = "Paris sportif - tennis"

TEAM_MEMBERS = [
    Member(
        name = "Alexandre Rouet",
        linkedin_url = "https://www.linkedin.com/in/charles-boudry-a6875b3a/",
        github_url = "https://github.com/chboudry"
    ),
    Member(
        name = "Charles Boudry",
        linkedin_url = "https://www.linkedin.com/in/charles-boudry-a6875b3a/",
        github_url = "https://github.com/chboudry"
    ),
    Member(
        name = "David Querin",
        linkedin_url = "https://www.linkedin.com/in/charles-boudry-a6875b3a/",
        github_url = "https://github.com/chboudry"
    ),
    Member(
        name = "Marielle Odile Gahungu",
        linkedin_url = "https://www.linkedin.com/in/charles-boudry-a6875b3a/",
        github_url = "https://github.com/chboudry"
    )        
]

PROMOTION = "Bootcamp Data Scientist - July 2023"

CO_UK_DATA_PATH = '../data_scrapped/co_uk_data.csv'

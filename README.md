# decred_contributor_track
This program is to track new decred contributors

Needs python3

Edit main.py add your oauth token get via "https://github.com/settings/tokens" only needs " Access public repositories " setting. 

Then simply run.

python3 main.py

CSV export:

python3 csv_export.py ---> dumps all
python3 csv_export.py "YYYY-MM-DD HH:MM"  ---> This will dump all users after specified date. 

use "https://sqlitebrowser.org/" to work with SQLITE database.

# decred_contributor_track

This program is to track new decred contributors and other activity on Decred GitHub repos.

Requirements

* python3
* mariadb

# Installation

Install required python modules:

```pip install -r requirements.txt```

## Create Database

Use the following commands to create a database and user. NOTE: the username/password is currently ```user/password``` (not very secure). 

```
CREATE DATABASE contributors CHARACTER SET UTF8;
CREATE USER user@localhost IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON contributors.* TO user@localhost;
FLUSH PRIVILEGES;
USE contributors;
```

# How to use

1. Edit ```main.py`` to add your oauth token (stored in token variable). You can create an access token in your [GitHub settings](https://github.com/settings/tokens). It only needs the " Access public repositories " setting.

2. Run the main script.

```python3 main.py```and 

This script fetches data from the GitHub API and stores it in the database.

3. (Optional) run the export script to output tables into csv files. 

```python3 csv_export.py```

4. (Optional) run the dev stats script to generate baseic repo-level statistsics (# commits, additions, deletions, total lines changed).

```python3 dev_stats.py```

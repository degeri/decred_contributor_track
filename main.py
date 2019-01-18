
import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime
# import sqlalchemy_utils 

from database import Base, engine, session

from sqlalchemy import ForeignKey
from functions import *


# ----------- Create db models ---------------

class Event(Base):
    __tablename__ = "event_log"

    id = Column(Integer, primary_key=True)
    type_id = Column(Integer, ForeignKey('event_types.id'))
    repo_id = Column(Integer, ForeignKey('repository_list.id'))
    github_username = Column(String(128))
    datetime = Column(DateTime, default=datetime.datetime.now)
    github_url = Column(String(128))

class Repo(Base):
    __tablename__ = "repository_list"

    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    organization = Column(String(128)) 

class Event_type(Base):
    __tablename__ = "event_types"

    id = Column(Integer, primary_key=True)
    event_type = Column(String(128))


# Create tables in db
Base.metadata.create_all(engine)


# ----------- Set session variables ---------------

token = 'YOUR-TOKEN'
username='decred'

# Repos to analyze
repos = ['politeia', 'dcrd', 'dcrwallet', 'dcrdata', 'dcrbounty', 'decrediton', 'dcrdocs']
repo = 'politeia'  # select this replo for now

event_types = ['commit', 'issue', 'pull_request', 'comment_on_comment', 'comment_on_pr', 'review']

# # ----------- Get list of all repos  ---------------

print('fetching repos...')
list_of_repos=get_all_repo(username,token)
# # repo = 
# for repo in list_of_repos:
#     contributors = (get_all_contributors(username, repo,token))

# ------------- Save repos id's into db -----------

for i in range(0,len(repos)):

  repo_entry = Repo()
  repo_entry.name = repos[i]
  repo_entry.organization = username
  session.add(repo_entry)
  session.commit()   


# ------------- Set event types into db -----------

for i in range(0,len(event_types)):

  event_type = Event_type()
  event_type.event_type = event_types[i]
  session.add(event_type)
  session.commit()                                                                                                                                                         


# ----------- Fetch commits repo -----------

print('fetching commits...')
all_commits = get_commits_repo(username,repo,token)

# Save commits in db
for commit in all_commits: 
  # print(commit['committer']['login'] ) 
  commit_event = Event()
  commit_event.type_id = 1
  commit_event.repo_id = 1 # NOTE HARDCODED BUT NEEDS TO BE DYNAMIC
  commit_event.github_username = commit['commit']['author']['name']
  commit_event.datetime = datetime.datetime.strptime(commit['commit']['author']['date'], "%Y-%m-%dT%H:%M:%SZ") 
  commit_event.github_url = commit['html_url']  # Note: this is the HTML url (can also do API call)
  session.add(commit_event)
  session.commit()  
  # print(commit['commit']['author']['name'] )  


# ----------- Fetch PRs repo -----------

state = 'all'  # (open, closed, all (default = open))
print('fetching PRs...')
all_pull_requests = get_pull_requests_repo(username,repo,state,token)

# save PRs in db
for pull_request in all_pull_requests: 

  pr = Event()
  pr.type_id = 3
  pr.repo_id = 1 # NOTE HARDCODED BUT NEEDS TO BE DYNAMIC
  pr.github_username = pull_request['user']['login'] 
  pr.datetime = datetime.datetime.strptime(pull_request['created_at'] , "%Y-%m-%dT%H:%M:%SZ")  #NOTE: using "created at" (can also do last modified)
  pr.github_url = pull_request['html_url']  # Note: this is the HTML url (can also do API call)
  session.add(pr)
  session.commit()  
  # print(pull_request['title'])  


# ----------- Fetch Issues repo -----------

state = 'all'  # (open, closed, all (default = open))
print('fetching Issues...')
all_issues = get_issues_repo(username,repo,state,token)

# save issues in db
for issue in all_issues: 

  issue_event = Event()
  issue_event.type_id = 2
  issue_event.repo_id = 1 # NOTE HARDCODED BUT NEEDS TO BE DYNAMIC
  issue_event.github_username = issue['user']['login'] 
  issue_event.datetime = datetime.datetime.strptime(issue['created_at'] , "%Y-%m-%dT%H:%M:%SZ")  #NOTE: using "created at" (can also do last modified)
  issue_event.github_url = issue['html_url']  # Note: this is the HTML url (can also do API call)
  session.add(issue_event)
  session.commit()  
  # print(issue['title'])  
    # print(issue['title'])  


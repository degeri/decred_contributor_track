import datetime
from sqlalchemy import Column, Integer, String, DateTime, exc, VARCHAR, select, ForeignKey, BLOB, LargeBinary #Text # JSON
from database import Base, engine, session
from functions import *
import json
import pickle

# ----------- Create db models ---------------

class Event(Base):
    __tablename__ = "event_log"

    id = Column(Integer, primary_key=True)
    type_id = Column(Integer, ForeignKey('event_types.id'))
    repo_id = Column(Integer, ForeignKey('repository_list.id'))
    github_username = Column(String(39)) # 39 is max len of github username
    datetime = Column(DateTime, default=datetime.datetime.now)
    github_url = Column(VARCHAR(255),unique=True) #2083 max len of a URL, but cannot use 'unique' hope this is enough.
    data = Column(LargeBinary)
    # data = Column(BLOB)

class Repo(Base):
    __tablename__ = "repository_list"

    id = Column(Integer, primary_key=True)
    name = Column(String(100),unique=True) #100 is max repo len
    organization = Column(String(39)) # 39 same as username.

class Event_type(Base):
    __tablename__ = "event_types"

    id = Column(Integer, primary_key=True)
    event_type = Column(String(128),unique=True)


# Create tables in db
Base.metadata.create_all(engine)


# ----------- Set session variables ---------------

token = '7e3334fba97b2763119da24cec0e5a98d3ee4f5c'
username='decred'
# username = 'raedahgroup'
# https://github.com/raedahgroup/


# # ----------- Get list of all repos  ---------------

print('fetching repos...')
#list_of_repos=get_all_repo(username,token) #for actual full list.
# list_of_repos = ['dcrd', 'decrediton', 'dcrweb', 'dcrwallet','dcrdata','dcrdocs','politeia'] #'dcrios',
# list_of_repos = ['politeia','politeiagui','dcrweb', 'dcrd', 'dcrwallet', 'dcrdata', 'decrediton', 'dcrdocs']
list_of_repos = ['politeia','politeiagui','dcrweb', 'dcrd', 'dcrwallet', 'dcrdata', 'decrediton', 'dcrdocs', 'dcrstakepool', 'atomicswap', 'dcrandroid', 'hardforkdemo', 'base58']
# list_of_repos = ['politeia']
# list_of_repos = ['dcrd']
# list_of_repos = ['dcrios', 'godcr'] #'dcrlibwallet','godcr']

# ------------- Save repos id's into db -----------

for i in range(0,len(list_of_repos)):
    print(list_of_repos[i])

    repo_entry = Repo()
    repo_entry.name = list_of_repos[i]
    repo_entry.organization = username
    try:
        session.add(repo_entry)
        session.commit()
    except exc.IntegrityError as err:
        session.rollback()

# ------------- Set event types into db -----------

event_types = ['commit', 'issue', 'pull_request', 'comment', 'review']

for i in range(0,len(event_types)):
    event_type = Event_type()
    event_type.event_type = event_types[i]
    try:
        session.add(event_type)
        session.commit()
    except exc.IntegrityError as err:
        session.rollback()

# --------------Load events from DB into a dictionary------------------------

select_event = select([Event_type])
event_result = session.execute(select_event)

event_dict = {}

for event_rows in event_result:
    event_dict[event_rows['event_type']] = event_rows['id']

# --------------- Fetch all repo from database--------------------------

select_repo = select([Repo])
repo_result = session.execute(select_repo)

# --------- Loop through fetched repos--------------

for repo_row in repo_result:
    repo_name = repo_row['name']
    repo_organization = repo_row['organization']
    repo_id = repo_row['id']
    print("Doing Repo " + repo_name)

    # ----------- Fetch commits repo -----------
    check_limit_wait(token)
    print('fetching commits ...')
    check_limit_wait(token)
    all_commits = get_commits_repo(username, repo_name, token)
    #Save commits in db
    for commit in all_commits:
        commit_event = Event()
        commit_event.type_id = event_dict['commit']
        commit_event.repo_id = repo_id
        commit_event.github_username = commit['commit']['author']['name']
        commit_event.datetime = datetime.datetime.strptime(commit['commit']['committer']['date'], "%Y-%m-%dT%H:%M:%SZ")
        commit_event.github_url = commit['html_url']  # Note: this is the HTML url (can also do API call)
        # commit_event.data = json.dumps(commit)
        commit_event.data = pickle.dumps(commit)
        try:
            session.add(commit_event)
            session.commit()
        except exc.IntegrityError as err:
            session.rollback()
        # print(commit['commit']['author']['name'] )

    # ----------- Fetch PRs repo -----------
    state = 'all'  # (open, closed, all (default = open))
    check_limit_wait(token)
    print('fetching PRs...')
    all_pull_requests = get_pull_requests_repo(username, repo_name, state, token)
    # save PRs in db
    for pull_request in all_pull_requests:

        pr = Event()
        pr.type_id = event_dict['pull_request']
        pr.repo_id = repo_id
        pr.github_username = pull_request['user']['login']
        pr.datetime = datetime.datetime.strptime(pull_request['created_at'],
                                                 "%Y-%m-%dT%H:%M:%SZ")  # NOTE: using "created at" (can also do last modified)
        pr.github_url = pull_request['html_url']  # Note: this is the HTML url (can also do API call)
        pr.data = pickle.dumps(pull_request)
        try:
            session.add(pr)
            session.commit()
        except exc.IntegrityError as err:
            session.rollback()


    # ----------- Fetch Issues repo -----------

    check_limit_wait(token)
    state = 'all'  # (open, closed, all (default = open))
    print('fetching Issues...')
    all_issues = get_issues_repo(username, repo_name, state, token)
    # save issues in db
    for issue in all_issues:

        issue_event = Event()
        issue_event.type_id = event_dict['issue']
        issue_event.repo_id = repo_id
        issue_event.github_username = issue['user']['login']
        issue_event.datetime = datetime.datetime.strptime(issue['created_at'],
                                                          "%Y-%m-%dT%H:%M:%SZ")  # NOTE: using "created at" (can also do last modified)
        issue_event.github_url = issue['html_url']  # Note: this is the HTML url (can also do API call)
        # issue_event.data = pickle.dumps(issue)
        try:
            session.add(issue_event)
            session.commit()
        except exc.IntegrityError as err:
            session.rollback()

    # ----------- Fetch comments on Issues -----------

    # state = 'all'  # (open, closed, all (default = open))
    check_limit_wait(token)
    print('fetching comments...')
    all_comments = get_comments_repo(username,repo_name,token)

    # save issues in db
    for comment in all_comments:

        comment_event = Event()
        comment_event.type_id = event_dict['comment']
        comment_event.repo_id = repo_id
        comment_event.github_username = comment['user']['login']
        comment_event.datetime = datetime.datetime.strptime(comment['created_at'] , "%Y-%m-%dT%H:%M:%SZ")  #NOTE: using "created at" (can also do last modified)
        comment_event.github_url = comment['html_url']  # Note: this is the HTML url (can also do API call)
        # comment_event.data = pickle.dumps(comment)

        try:
            session.add(comment_event)
            session.commit()
        except exc.IntegrityError as err:
            session.rollback()

    # ----------- Fetch comments on PRs (reviews) -----------

    # state = 'all'  # (open, closed, all (default = open))
    check_limit_wait(token)
    print('fetching comments PRs (reviews)...')
    all_comments = get_comments_prs_repo(username,repo_name,token)

    # save issues in db
    for comment in all_comments:

        comment_event = Event()
        comment_event.type_id = event_dict['review']
        comment_event.repo_id = repo_id
        comment_event.github_username = comment['user']['login']
        comment_event.datetime = datetime.datetime.strptime(comment['created_at'] , "%Y-%m-%dT%H:%M:%SZ")  #NOTE: using "created at" (can also do last modified)
        comment_event.github_url = comment['html_url']  # Note: this is the HTML url (can also do API call)
        comment_event.data = pickle.dumps(comment)
        try:
            session.add(comment_event)
            session.commit()
        except exc.IntegrityError as err:
            session.rollback()
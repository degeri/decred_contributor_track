from database import Base, engine, session
import csv
from functions import *

# Get list of repositories in database
r = session.execute('SELECT * FROM repository_list;') 

additions_total = 0
deletions_total = 0

repos = []
open_prs = []
additions_v = []
deletions_v = []
open_prs_v = []
commits_v = []

list_of_repos = ['dcrdocs']

for repo in r:

	repos.append(repo["name"])
	# repos.append(repo)

	check_limit_wait(token) # Check to see if over API rate limit
	# fetch commits
	c = session.query(Event).filter(Event.type_id==1, Event.repo_id==repo["id"], Event.datetime >  "2019-03-01", Event.datetime < "2019-04-01").all()  
	# c = session.query(Event).filter(Event.type_id==1, Event.repo_id==1, Event.datetime >=  "2019-03-01", Event.datetime <= "2019-04-01").all()  

	additions = 0
	deletions = 0
	commits = 0

	for commit in c:

		# Fetch commit from github from commit hash
		commit_hash = pickle.loads(commit.data)["sha"] 
		commit = requests.get("https://api.github.com/repos/"+username+"/"+repo["name"]+"/commits/"+commit_hash, auth=(username,token))
		# commit = requests.get("https://api.github.com/repos/"+username+"/"+repo+"/commits/"+commit_hash, auth=(username,token))

		additions += commit.json()['stats']['additions']  
		deletions += commit.json()['stats']['deletions'] 
		commits += 1

	# print(repo["name"])
	print(repo)
	print("additions: " + str(additions))
	print("deletions: " + str(deletions))

	additions_v.append(additions)
	deletions_v.append(deletions)
	commits_v.append(commits)

	additions_total += additions
	deletions_total += deletions 


	# fetch open PRs
	check_limit_wait(token) # Check to see if over API rate limit
	p = session.query(Event).filter(Event.type_id==3, Event.repo_id==repo["id"], Event.datetime >=  "2019-03-01", Event.datetime <= "2019-04-01").all()  
	# p = session.query(Event).filter(Event.type_id==3, Event.repo_id==1, Event.datetime >=  "2019-03-01", Event.datetime <= "2019-03-31").all() 

	open_prs = 0

	for pr in p:
		pull_request = pickle.loads(pr.data)
		# print(pull_request['state'])
		print(state)
		if pull_request['state'] == 'open':
			open_prs += 1

	open_prs_v.append(open_prs)

print(repo)


i = 0

for i in range(len(repos)):

	print("repo: "+ repos[i])
	print("additions: " + str(additions_v[i]))
	print("deletions: " + str(deletions_v[i]))
	print("total changes: " + str(additions_v[i]+deletions_v[i]))
	print("commits master: " + str(commits_v[i]))
	print("open PRs: " + str(open_prs_v[i])+"\n")
	







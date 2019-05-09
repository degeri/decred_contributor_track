from database import Base, engine, session
import csv
from functions import *
from main import *


start_date = datetime.datetime.strptime('4/1/2019', '%m/%d/%Y')
end_date = datetime.datetime.strptime('5/1/2019', '%m/%d/%Y')

# Get list of repositories in database
r = session.execute('SELECT * FROM repository_list;') 

additions_total = 0
deletions_total = 0
commits_total = 0
active_prs_total = 0
repos_total = 0

repos = []
active_prs = []
additions_v = []
deletions_v = []
open_prs_v = []
active_prs_v = []
commits_v = []


# For each repo, calculate dev stats
for repo in r:

	repos.append(repo["name"])
	# repos.append(repo)

	# Query commits and calculate # commits, additions/deletions
	check_limit_wait(token) # Check to see if over API rate limit

	# fetch commits
	c = session.query(Event).filter(Event.type_id==1, Event.repo_id==repo["id"], Event.datetime >  "2019-04-01", Event.datetime < "2019-05-01").all()  
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

	repos_total += 1
	commits_total += commits
	additions_total += additions
	deletions_total += deletions 

	check_limit_wait(token) # Check to see if over API rate limit

	# Query PRs and calculate # active
	p = session.query(Event).filter(Event.type_id==3, Event.repo_id==repo["id"]).all() 

	active_prs = 0

	for pr in p:
		pull_request = pickle.loads(pr.data)

		created_date = datetime.datetime.strptime(pull_request['created_at'],"%Y-%m-%dT%H:%M:%SZ")  # NOTE: using "created at" (can also do last modified)

		if pull_request['state'] == 'open' and \
			(created_date >= start_date and created_date <= end_date):

			 active_prs += 1

		if pull_request['state'] == 'closed' and pull_request['merged_at']:
			merged_at = datetime.datetime.strptime(pull_request['merged_at'],"%Y-%m-%dT%H:%M:%SZ") 

			if (merged_at >= start_date and merged_at <= end_date):
				active_prs += 1
				merged_prs += 1

	active_prs_total += active_prs
	active_prs_v.append(active_prs)


# Calculate stat totals

i = 0
total_additions = 0
total_deletions = 0
total_active_prs = 0
total_commits = 0
total_repos = 0

for i in range(len(repos)):

	print("repo: "+ repos[i])
	print("additions: " + str(additions_v[i]))
	print("deletions: " + str(deletions_v[i]))
	print("total changes: " + str(additions_v[i]+deletions_v[i]))
	print("commits master: " + str(commits_v[i]))
	print("active PRs: " + str(active_prs_v[i])+"\n")
	# print("open PRs: " + str(open_prs_v[i])+"\n")

	total_additions += additions_v[i]
	total_deletions += deletions_v[i]
	total_active_prs += active_prs_v[i]
	total_commits += commits_v[i]
	total_repos += 1


print("total additions (all repos): " + str(total_additions))
print("total deletions (all repos): " + str(total_deletions))
print("total commits (all repos): " + str(total_commits))
print("total active PRs (all repos): " + str(total_active_prs))
print("total repos: " + str(total_repos))



import json, requests, csv


# Get all repos for a given user/org
def get_all_repo(user,token):
    all_repo = []
    pageno=1
    while True:
        response = requests.get("https://api.github.com/users/"+user+"/repos?page="+str(pageno)+'&access_token='+token+"&per_page=100")
        for r in response.json():
            all_repo.append(r['name'])
        if 'next' in response.links:
            pageno = pageno + 1
        else:
            break
    return all_repo

# Get all contributors for a given repo
def get_all_contributors(user,repo,token):
    all_contri = []
    pageno=1
    while True:
        response = requests.get("https://api.github.com/repos/"+user+"/"+repo+"/contributors?page="+str(pageno)+'&access_token='+token+"&per_page=100")
        for r in response.json():
            all_contri.append(r['login'])
        if 'next' in response.links:
            pageno = pageno + 1
        else:
            break
    return all_contri

# Get all commits for a given repo 
def get_commits_repo(user,repo,token):

    pageno = 0

    commits = requests.get("https://api.github.com/repos/"+user+"/"+repo+"/commits?page="+str(pageno)+'&access_token='+token+"&per_page=100")

    # Iterate through all pages to get rest of commits
    all_commits = commits.json()
    while 'next' in commits.links.keys():
        pageno += 1
        commits = requests.get("https://api.github.com/repos/"+user+"/"+repo+"/commits?page="+str(pageno)+'&access_token='+token+"&per_page=100")
        all_commits.extend(commits.json())

    return all_commits 

# Get all PRs for a given repo 
def get_pull_requests_repo(user,repo,state,token):

    pageno = 0
    pull_requests = requests.get("https://api.github.com/repos/"+user+"/"+repo+"/pulls?state="+state+"&page="+str(pageno)+'&access_token='+token+"&per_page=100")

    all_pull_requests = pull_requests.json()
    while 'next' in pull_requests.links.keys():
        pageno += 1
        pull_requests = requests.get("https://api.github.com/repos/"+user+"/"+repo+"/pulls?page="+str(pageno)+'&access_token='+token+"&per_page=100")
        all_pull_requests.extend(pull_requests.json())

    return all_pull_requests

# Get all PRs for a particular repo 
def get_issues_repo(user,repo,state,token):

    pageno = 0

    issues = requests.get("https://api.github.com/repos/"+user+"/"+repo+"/issues?state="+state+"&page="+str(pageno)+'&access_token='+token+"&per_page=100")
    all_issues = issues.json()
    while 'next' in issues.links.keys():
        pageno += 1
        issues = requests.get("https://api.github.com/repos/"+user+"/"+repo+"/issues?state="+state+"&page="+str(pageno)+'&access_token='+token+"&per_page=100")
        all_issues.extend(issues.json())

    return all_issues

# Get all comments 
def get_comments_repo(user,repo,token):

    pageno = 0

    comments = requests.get("https://api.github.com/repos/"+user+"/"+repo+"/issues/comments?page="+str(pageno)+'&access_token='+token+"&per_page=100")
    all_comments = comments.json()
    while 'next' in comments.links.keys():
        pageno += 1
        comments = requests.get("https://api.github.com/repos/"+user+"/"+repo+"/issues/comments?page="+str(pageno)+'&access_token='+token+"&per_page=100")
        all_comments.extend(comments.json())

    return all_comments

# Get all comments on PRs (reviews) 
def get_comments_prs_repo(user,repo,token):

    pageno = 0

    comments = requests.get("https://api.github.com/repos/"+user+"/"+repo+"/pulls/comments?page="+str(pageno)+'&access_token='+token+"&per_page=100")
    all_comments = comments.json()
    while 'next' in comments.links.keys():
        pageno += 1
        comments = requests.get("https://api.github.com/repos/"+user+"/"+repo+"/pulls/comments?page="+str(pageno)+'&access_token='+token+"&per_page=100")
        all_comments.extend(comments.json())

    return all_comments


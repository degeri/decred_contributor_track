import json, requests, csv




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



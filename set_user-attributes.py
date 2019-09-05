import requests
import json

# Mattermost server
url = "http://54.84.158.232:8065"
login_url = url+"/api/v4/users/login"
team_name = "demoteam"

def login(login_url):
    payload = { "login_id": "admin@mattermost.com",
                "password": "MattermostDemo,1"}
    headers = {"content-type": "application/json"}
    s = requests.Session()
    r = s.post(login_url, data=json.dumps(payload), headers=headers)
    auth_token = r.headers.get("Token")
    global hed
    hed = {'Authorization': 'Bearer ' + auth_token}

def search_user():
    login(login_url)
    print("after login...")
    post_url = url+"/api/v4/users/search"
    payload = {
        "term": "admin",
    }
    response = requests.post(post_url, headers=hed, json=payload)
    info = response.json()
    get_user(info[0]['id'])

def get_user(id):
    login(login_url)
    post_url = url+"/api/v4/users/"+id
    response = requests.get(post_url, headers=hed)
    info = response.json()
    print(info.items())
    for k, v in info.items():
        if k == 'create_at':
            print(v)
            create_at=v
            set_notification(id, create_at)

def set_notification(id, create_at):
    login(login_url)
    print("Set notification rule...")
    post_url = url+"/api/v4/users/"+id+"/patch"
    print(post_url)
    payload = {
        "id": id,
        "create_at": create_at,
        "notify_props": {
                "email": "false",
                "push": "none"
            }
    }
    print(payload)
    response = requests.put(post_url, headers=hed, json=payload)
    info = response.json()
    print info

search_user()

import requests
import json
from flask import Flask, request, redirect, url_for, jsonify
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

with open('config.json') as config_file:
    oauth = json.load(config_file)

# OAuth configuration
# Step 1: Redirect users to request Wunderlist access
@app.route('/')
def root():
    uri = oauth['authentication_url'] % (oauth['client_id'], oauth['callback_url'])
    return redirect(uri)

# Step 2: If user accepts, Wunderlist redirects here
@app.route('/callback/wunderlist', methods=["GET"])
def callback_function():
    code = request.args.get('code')
    uri = oauth['token_url']
    params = {
        'client_id': oauth['client_id'],
        'client_secret': oauth['client_secret'],
        'code': code,
        'grant-type': 'authorization_code',
        'redirect_uri': oauth['callback_url']
    }
    response = requests.post(uri, json=params).json()
    oauth['token'] = response['access_token']
    return redirect(url_for('userinfo'))

# Helper functions to GET and POST information
def get_from_api(get_uri, headers=None):
    if not headers:
        headers = {
            'access_token': oauth['token'],
            'client_id': oauth['client_id']
        }
    else:
        headers['access_token'] = oauth['token']
        headers['client_id'] = oauth['client_id']
    response = requests.get(get_uri, headers)
    return response.json()

def post_to_api(post_uri, payload):
    headers = {
        'X-Access-Token' : oauth['token'],
        'X-Client-ID' : oauth['client_id'],
    }
    response = requests.post(post_uri, json=payload, headers=headers)
    return response.json()

class UserInfo(Resource):
    user_url = 'https://a.wunderlist.com/api/v1/user'

    def get(self):
        response = get_from_api(self.user_url)
        return jsonify(response)

class UserLists(Resource):
    lists_url = 'https://a.wunderlist.com/api/v1/lists'

    def get(self):
        response = get_from_api(self.lists_url)
        return jsonify(response)

    def post(self):
        payload = request.get_json()
        response = post_to_api(self.lists_url, payload)
        return jsonify(response)

class Tasks(Resource):
    tasks_url = 'https://a.wunderlist.com/api/v1/tasks'

    def get(self, list_id, completed):
        payload = {
            'completed': completed,
            'list_id': list_id
        }
        response = get_from_api(self.tasks_url, payload)
        return jsonify(response)
    
    def post(self, list_id, completed):
        payload = request.get_json()
        payload['list_id'] = int(list_id)
        if completed:
            payload['completed'] = True
        else:
            payload['completed'] = False
        print(payload)
        response = post_to_api(self.tasks_url, payload)
        return jsonify(response)

api.add_resource(UserInfo, '/user_info')
api.add_resource(UserLists, '/user_lists')
api.add_resource(Tasks, '/tasks/list_id=<list_id>&completed=<completed>')

if __name__ == '__main__':
    app.run()

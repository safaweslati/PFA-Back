from flask import Flask, request, jsonify
import requests
import json
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

with open('config.json', 'r') as f:
    config = json.load(f)

instagram_account_id = config['instagram_account_id']
access_token = config['access_token']

@app.route('/predict', methods=['POST'])
def predict():
     try:
        username = request.json.get('username')
        user_data = get_user_info_and_posts(username, instagram_account_id, access_token)

        user_interests = {
            'Category 1': ['Interest 1', 'Interest 2'],
            'Category 2': ['Interest 3', 'Interest 4']
         }
        return jsonify(user_interests)
     
     except Exception as e:
        print('Error:', e)
        return jsonify(error='Internal Server Error'), 500
    
def get_user_info_and_posts(username, instagram_account_id, access_token):
    ig_params = {
        'fields': 'business_discovery.username(' + username + '){name,media.limit(100){media_type,thumbnail_url,media_url,caption}}',
        'access_token': access_token
    }
    endpoint = f"https://graph.facebook.com/v19.0/{instagram_account_id}"
    response = requests.get(endpoint, params=ig_params)
    return format_response(response.json())

def format_response(response):
    user = {}
    try:
        business_discovery_data = response.get('business_discovery', {})
        user['username'] = business_discovery_data.get('name', '')
        user['user_id'] = business_discovery_data.get('id', '')
        user['posts'] = business_discovery_data.get('media', {}).get('data', [])
    except KeyError as e:
        print("KeyError:", e)
    return user

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, request, redirect, session, jsonify
import os
import requests
import jwt

from data_storage import StoreData

app = Flask(__name__)
app.secret_key = os.urandom(25)

redirect_uri = ''
response_type = 'authorization_code'

client_id=''
# client_secret = ''
auth_link = f"https://api.idmelabs.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope=openid http://idmanagement.gov/ns/assurance/ial/2/aal/2&eid=555"

@app.route('/')
def index():

    """Direct users to authorization endpoint"""

    return redirect(auth_link)

@app.route('/idme', methods=['GET'])
def callback():

    """Handle callback, extract authorization code, proceed"""

    auth_code = request.args.get('code')
    if auth_code:
        session['auth_code'] = auth_code
        print(f'Authorization code: {auth_code}\n')

        token_payload_url = f"https://api.idmelabs.com/oauth/token"
        
        # Payload params
        payload = {
            'code': auth_code,
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code'
        }
        
        # Exchange authentication code for token payload
        response = requests.post(token_payload_url, data=payload)

        if response.status_code == 200:
            token_payload = response.json()
            print(f'Token payload: {token_payload}\n')

            id_token = token_payload['id_token']
            if id_token:
                decoded_id_token = jwt.decode(id_token, options={"verify_signature": False})
                print(f'Decoded id_token: {decoded_id_token}\n')
                payload = decoded_id_token

                # initialize the StoreData class and pass in payload
                data_storage = StoreData(payload)

                # store data
                data_storage.save_json()
                data_storage.save_csv()

                return payload

        return f'Authentication completed! Authorization code: {auth_code}'

    else:
        return 'Authentication failed.'

if __name__ == '__main__':
    app.run(port=3000, debug=True)
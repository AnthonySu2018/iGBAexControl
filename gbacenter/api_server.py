
from flask import Flask, request, jsonify
import secrets
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


app = Flask(__name__)
app.json.ensure_ascii=False
tokens = {}
users = {'your_username': 'your_password'}


@app.route('/get_token', methods=['POST'])
def get_token():
    # print(request.get_json())
    username = request.json.get('username')
    password = request.json.get('password')
    if username in users and users[username] == password:
        token = secrets.token_hex(16)
        tokens[username] = token
        print(token)
        print('ok')
        return jsonify({'token': token}), 200
    else:
        return jsonify({'message': 'Authentication failed'}), 401


@app.route('/send_command', methods=['POST'])
def send_command():
    token = request.headers.get('Authorization').split()[1]
    print('haha')
    print(token)
    command = request.json.get('command')
    # print(request.headers)
    for username, user_token in tokens.items():
        if user_token == token:
            print(command)
            return jsonify({'message': f"Executing '{command}' as {username}"}), 200

    return jsonify({'message': 'Invalid token'}), 401


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=False)

import requests


def get_token(username, password):
    response = requests.post('http://127.0.0.1:5000/get_token', json={'username': username, 'password': password})
    if response.status_code == 200:
        return response.json()['token']
    else:
        return None


def send_command(token, command):
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.post('http://127.0.0.1:5000/send_command', headers=headers, json={'command': command})
    print(response.headers)
    if response.status_code == 200:
        return response.json()['message']
    else:
        return 'Command failed'


if __name__ == '__main__':
    username = 'your_username'
    password = 'your_password'
    command = {'类型':'展厅介绍','区域':'序厅','控制':''}

    token = get_token(username, password)
    print(token)
    if token:
        result = send_command(token, command)
        print(result)
    else:
        print('Authentication failed')


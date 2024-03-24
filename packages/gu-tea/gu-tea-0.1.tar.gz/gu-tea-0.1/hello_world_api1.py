import requests

def fetch_hello_world():
    response = requests.get('https://api.github.com')
    print(response.json()['current_user_url'])

if __name__ == "__main__":
    fetch_hello_world()

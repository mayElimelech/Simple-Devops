import requests
URL="https://simple-devops.onrender.com/"
def pingServer():
    try:
        respons=requests.get(URL)
        print(f"pinged to server {respons.status_code}")
    except Exception as e:
        print("failed to ping server:", e)
if __name__ == '__main__':
    pingServer()
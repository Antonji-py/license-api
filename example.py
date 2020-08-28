import requests
import socket

key = input("Please input you license key: ")
user_ip = socket.gethostbyname(socket.gethostname())

response = requests.get(f"http://127.0.0.1:5000/authorize/{key}/{user_ip}")

if response["status"] == 1:
    print("The license is valid!")
else:
    print(f"The license does not work: {response['message']}")
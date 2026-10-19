
import requests

url = "https://johnmichaelpabilona.onrender.com/student"

try:
    response = requests.get(url, timeout=60)

    print("Status Code:", response.status_code)

    if response.status_code == 200:
        data = response.json()

        print("Classmate's API Data")
        print(data)

    else:
        print("Request failed.")
        print(response.text)

except requests.RequestException as error:
    print("Connection error:", error)

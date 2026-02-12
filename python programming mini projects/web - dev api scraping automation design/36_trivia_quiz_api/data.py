import requests

parameters = {"amount": 20, "type": "boolean"}  # "category": 18 - computers questions

response = requests.get(url="https://opentdb.com/api.php", params=parameters)
# print(response)
# print(response.status_code)
response.raise_for_status()
data_json = response.json()
question_data = data_json["results"]
# print(question_data)

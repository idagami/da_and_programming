# documentation: https://docs.pixe.la/

import requests, datetime

USER_NAME = "irenadav"
TOKEN = "hgjA?3o8Ak3"
USER_ENDPOINT = "https://pixe.la/v1/users"
user_parameters = {
    "token": TOKEN,
    "username": USER_NAME,
    "agreeTermsOfService": "yes",
    "notMinor": "yes",
}

## below part is run once to create user, then we comment it so it doesnt run again,
## as system wont let us create account with same username
# response = requests.post(USER_ENDPOINT, json=user_parameters)
# print(response.text) # we only want the response status = .text

GRAPH_ENDPOINT = f"{USER_ENDPOINT}/{USER_NAME}/graphs"
graph_parameters = {
    "id": "graph1",
    "name": "Irenka's reading tracker",
    "unit": "page",
    "type": "int",
    "color": "ajisai",
}

headers_data = {"X-USER-TOKEN": TOKEN}

## below part is run once to create graph, then we comment it so it doesnt run again,
## as system wont let us create same graph
# response = requests.post(
#     url=GRAPH_ENDPOINT, json=graph_parameters, headers=headers_data
# )
# print(response.text)

# now can see my graph at https://pixe.la/v1/users/irenadav/graphs/graph1 https://pixe.la/v1/users/irenadav/graphs/graph1.html

PIXEL_ENDPOINT = f"{USER_ENDPOINT}/{USER_NAME}/graphs/graph1"

today_full = datetime.datetime.now()
date_full = datetime.datetime(
    year=2025, month=9, day=21
)  # if i want to post data for any day other than today
date_str = datetime.datetime.strftime(
    date_full, "%Y%m%d"
)  # alternatively: today_date = datetime.datetime.now().date() today_date_str = (str(today_date)).replace("-", "")
# print(today_date_str)

pixel_parameters = {"date": date_str, "quantity": "1"}

# # below part is run once to post pixel for specific day, then we comment it so it doesnt run again,
# # as system WILL let us create pixel (=entry) for the same date - it will overwrite the old info
# response = requests.post(
#     url=PIXEL_ENDPOINT, json=pixel_parameters, headers=headers_data
# )
# print(response.text)


UPD_PIXEL_ENDPOINT = f"{USER_ENDPOINT}/{USER_NAME}/graphs/graph1/{date_str}"
upd_pixel_parameters = {"quantity": "22"}

response = requests.put(
    UPD_PIXEL_ENDPOINT, json=upd_pixel_parameters, headers=headers_data
)
print(response.text)

# # below part is run once to post pixel for specific day, then we comment it so it doesnt run again,
# # as system wont let us delete pixel (=entry) for the same date
# response = requests.delete(UPD_PIXEL_ENDPOINT, headers=headers_data)
# print(response.text)

edit_params = {"color": "shibafu"}
# response = requests.put(PIXEL_ENDPOINT, json=edit_params, headers=headers_data)
# print(response.text)

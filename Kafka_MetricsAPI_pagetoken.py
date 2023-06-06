import httpx
import json
from requests.auth import HTTPBasicAuth

# Define authentication token and JSON
auth = HTTPBasicAuth('API-KEY', 'API-SECRET')
data = {
    "aggregations": [
        {
            "metric": "io.confluent.kafka.server/retained_bytes"
        }
    ],
    "filter": {
        "field": "resource.kafka.id",
        "op": "EQ",
        "value": "lkc-#####"
    },
    "granularity": "P1D",
    "group_by": [
        "metric.topic"
    ],
    "intervals": [
        "2023-04-17T00:00:00Z/PT1H"
    ]
}
new_data = {
    "aggregations": [
        {
            "metric": "io.confluent.kafka.server/retained_bytes"
        }
    ],
    "filter": {
        "field": "resource.kafka.id",
        "op": "EQ",
        "value": "lkc-#####"
    },
    "granularity": "P1D",
    "group_by": [
        "metric.topic"
    ],
    "intervals": [
        "2023-04-17T00:00:00Z/PT1H"
    ]
}
# Define static headers and base url, create token and response list
header = {"Content-Type": "application/json"}
token_list = []
all_responses = []
base_url = 'https://api.telemetry.confluent.cloud/v2/metrics/cloud/query'

# Send initial request
initial_post_response = httpx.post(base_url, headers=header, json=data, auth=auth)
initial_post_text = json.loads(initial_post_response.text)


# Take in the initial response, check if there is a "meta" key. If so, check if there's a nested "next_page_token" key
# Grab the page token, append it to my list, create a new URL for future queries
# Send the new response with a page_next_token appended
# Recursively repeat the above until there is no "next_page_token" keys
def recurse_pages(resp):
    if 'meta' in resp and 'next_page_token' in resp['meta']['pagination']:
        my_page_token = resp['meta']['pagination']['next_page_token']
        token_list.append(my_page_token)
        next_page_url = base_url + '?page_token=' + my_page_token
        response = httpx.post(next_page_url, headers=header, json=data, auth=auth)
        if check_validity(response):
            resp = json.loads(response.text)
            all_responses.append(resp)
            recurse_pages(resp)
    else:
        print("Reached the end of Metrics API results")


# Check for a successful (200) response from httpx
def check_validity(response: httpx.Response):
    if response.is_success:
        return True


# Check if we have a successful response (ex: 200), if so continue.
if check_validity(initial_post_response):
    all_responses.append(initial_post_text)
    recurse_pages(initial_post_response)
    print(f"Tokens: {token_list}")
    print(f"Responses: {all_responses}")
else:
    # If error, print
    print(initial_post_response.text)

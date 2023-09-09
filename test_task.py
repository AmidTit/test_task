import requests
import json
import base64
import git_api



# get data.json
data_url = "https://api.github.com/repos/thewhitesoft/student-2023-assignment/contents/data.json"
response1 = requests.get(data_url, auth=(git_api.username, git_api.token))

data = response1.text
json_data = json.loads(data)

decoded_bytes = base64.b64decode(json_data["content"])
decoded_str = decoded_bytes.decode("ascii")
data_json = json.loads(decoded_str)

with open("data.json", "w" ) as file:
    json.dump(data_json, file, indent=2)


# get replacement.json
replacement_url = "https://api.github.com/repos/thewhitesoft/student-2023-assignment/contents/replacement.json"
response2 = requests.get(replacement_url, auth=(git_api.username, git_api.token))

data = response2.text
json_data = json.loads(data)

decoded_bytes = base64.b64decode(json_data["content"])
decoded_str = decoded_bytes.decode("ascii")
replacement_json = json.loads(decoded_str)

with open("replacement.json", "w" ) as file:
    json.dump(replacement_json, file, indent=2)


   
# doing replacements
none_set = set()

for i in range(-1, -len(replacement_json) - 1 , -1):
    replacement = replacement_json[i]["replacement"]
    source = replacement_json[i]["source"]

    for j in range(len(data_json)):
        string = data_json[j]

        if replacement in string and source != None:
            new_string = string.replace(replacement, source)
            data_json[j] = data_json[j].replace(string, new_string)

        elif replacement in string and source == None:
            none_set.add(string)

result = [item for item in data_json if item not in none_set]

#upload the result.json
with open("result.json", "w") as f:
    json.dump(result, f, indent=2)

   

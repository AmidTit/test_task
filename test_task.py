import requests
import json
import base64
import git_api


def get_file(file_url):
        
        response = requests.get(file_url, auth=git_api.auth)
        data = response.text

        return json.loads(data)


def decode_file(json_data):

        decoded_bytes = base64.b64decode(json_data["content"])
        decoded_str = decoded_bytes.decode("ascii")

        return json.loads(decoded_str)
    

def upload_file(file_name, uploadable_file):
        with open(file_name + ".json" , "w") as file:
            json.dump(uploadable_file, file, indent = 2)
            

def do_replacement(replacements_json, data_json):

    none_set = set()  

    for i in range(-1, -len(replacements_json) - 1 , -1):
        
        replacement = replacements_json[i]["replacement"]
        source = replacements_json[i]["source"]

        for j in range(len(data_json)):

            string = data_json[j]

            if replacement in string and source != None:

                changed_string = string.replace(replacement, source)
                data_json[j] = data_json[j].replace(string, changed_string)

            elif replacement in string and source == None:

                none_set.add(string)

    return [item for item in data_json if item not in none_set]                 


# Точка входа в программу
if __name__ == "__main__":

    data_url = "https://api.github.com/repos/thewhitesoft/student-2023-assignment/contents/data.json"
    data_json = decode_file(get_file(data_url))
    upload_file("data", data_json)

    
    replacements_url = "https://api.github.com/repos/thewhitesoft/student-2023-assignment/contents/replacement.json"
    replacements_json = decode_file(get_file(replacements_url))
    upload_file("replacement", replacements_json)

    result = do_replacement(replacements_json, data_json)
    upload_file("result", result)

   

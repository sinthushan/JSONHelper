import requests
import json

def clean_output(response_data, n = 4):
    indents = '&nbsp' * n
    cleaned_output = ""
    if type(response_data) == dict:
        cleaned_output = cleaned_output + "{"
        for key in response_data:
            cleaned_output = cleaned_output + "<br>" + indents + key + ": " + clean_output(response_data[key], n *2)
        cleaned_output = cleaned_output + "<br>" + indents[len(indents)/2] + "}"
    elif type(response_data) == list:
        cleaned_output = cleaned_output + "["
        for element in response_data:
            cleaned_output = cleaned_output + "<br>" + indents  + clean_output(element, n *2)
        cleaned_output = cleaned_output + "<br>" + indents[len(indents)/2]  + "]"
    else:
        cleaned_output = cleaned_output + str(response_data) + ","
    return cleaned_output



# Create parameterized url
request_url = "http://api.worldbank.org/v2/country/all/indicator/NY.GDP.MKTP.CD?format=json"

# Submit request and format output
response_data = requests.get(request_url).json()


clean_output(response_data)
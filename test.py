import requests
import json

def clean_output(response_data, n = 4, python_trace = ""):
    indents = '&nbsp' * n
    cleaned_output = ""
    if type(response_data) == dict:
        cleaned_output = cleaned_output + "{"
        for key in response_data:
            python_trace = python_trace + "key:" +  key + ";" 
            cleaned_output = cleaned_output + "<br>" + indents + key + ": " + clean_output(response_data[key], n *2, python_trace)
            python_trace = ""
        cleaned_output = cleaned_output[:-1] + "<br>" + indents[:int(len(indents)/2)] + "},"
    elif type(response_data) == list:
        cleaned_output = cleaned_output + "["
        for index, element in enumerate(response_data):
            python_trace = python_trace + "index:" +  str(index) + ";"
            cleaned_output = cleaned_output + "<br>" + indents  + clean_output(element, n *2, python_trace)
            python_trace = ""
        cleaned_output = cleaned_output[:-1] + "<br>" + indents[:int(len(indents)/2)]  + "],"
    else:
        cleaned_output = cleaned_output + f'<span id="{python_trace[:-1]}">' + str(response_data) + '</span>,'
    return cleaned_output



# Create parameterized url
request_url = "http://api.worldbank.org/v2/country/all/indicator/NY.GDP.MKTP.CD?format=json"

# Submit request and format output
response_data = requests.get(request_url).json()


clean_output(response_data)
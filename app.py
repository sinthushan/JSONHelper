from flask import Flask, render_template, request, jsonify, redirect, url_for

import requests
import json

app = Flask(__name__)


@app.route('/', methods=['Post', 'Get'])
def index(json_path = ""):
    if request.method == 'POST':
        API_URL = request.form['API_URL'] #retrieving the URL inputted by User
        response_data = requests.get(API_URL).json() # retrieveing JSON data
        json_output = clean_output(response_data)[:-1]
        # We pass the modified JSON output to the template
        # the reason we pass the URL as well is to be able to reference when constructing
        # the python code
        return render_template('index.html', API_URL = API_URL,json_output =  clean_output(response_data)[:-1] )
    return render_template('index.html', API_URL = "",json_output= "" )

def clean_output(response_data, n = 4, python_trace = ""):
    '''
        This Function is recursive. The purpose of this function is to take JSON data and convert it into
        a visually digestable html output where the data points have the various keys and/or list indexes needed to
        reference them in their ID. Theses data points would be converted into clickable links which will trigger
        python code to be outputted.
    '''
    indents = '&nbsp' * n # setting the default indent of n spaces
    cleaned_output = ""
    if type(response_data) == dict:
        cleaned_output = cleaned_output + "{" #if the object type is a dict we add a { to the string
        for key in response_data:
            python_trace = python_trace + "key:" +  key + ";" # we will use the ; as a delimeter when constructint the python code
            # we are constructing a path to the data point whenever we encounter a dictionary we add the key
            # the value for the key is then passed through the function
            # the recursion breaks when the data type of the value is not a dictionary nor list
            cleaned_output = cleaned_output + "<br>" + indents + key + ": " + clean_output(response_data[key], n *2, python_trace)
            # At this point the last object is the key to a data point when we start constructing the path for the
            # next data point we want to remove the last key in the path
            python_trace = ";".join(python_trace[:-1].split(";")[:-1]) + ";" 
            if len(python_trace) == 1:
                python_trace = ""
        # Once we exhausted the dictionary we remove the extra comma the code created and then add
        # the closing curly bracket 
        cleaned_output = cleaned_output[:-1] + "<br>" + indents[:int(len(indents)/2)] + "},"
    elif type(response_data) == list:
        cleaned_output = cleaned_output + "[" #if the object type is a list we add a [ to the string
        for index, element in enumerate(response_data):
            python_trace = python_trace + "index:" +  str(index) + ";"
            cleaned_output = cleaned_output + "<br>" + indents  + clean_output(element, n *2, python_trace)
            python_trace = ";".join(python_trace[:-1].split(";")[:-1]) + ";" 
            if len(python_trace) == 1:
                python_trace = ""
        cleaned_output = cleaned_output[:-1] + "<br>" + indents[:int(len(indents)/2)]  + "],"
    else:
        # When it is determined the element is not a dictionary or list object
        # we conclude that we have reached an endpoint and create a link with the path in the ID
        cleaned_output = cleaned_output + f'<a href = "#" id="{python_trace[:-1]}">' + str(response_data) + '</a>,'
    return cleaned_output

@app.route('/_JSONPATH')
def get_python_code():
    '''
        This Function creates a string of Python code needed to access the clicked data point
        We are dynamically updating the page using jQuery.
    '''
    json_path = request.args.get('json_path', 0, type=str)
    API_URL = request.args.get('API_URL', 0, type=str)
    JSON_path_lst = json_path.split(';')
    python_code = f"<p>Python Code:</p> import requests <br> import json <br> API_URL = '{API_URL}' <br> response_data = requests.get(API_URL).json() <br> response_data"
    for key_index in JSON_path_lst:
        index = key_index.split(":")[1]
        if index.isnumeric():
            python_code = python_code + f"[{index}]"
        else:
            python_code = python_code + f"['{index}']"
    return jsonify(result = python_code) # output converted to JSON in order to be used by jQuery code

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request
import requests
import json
app = Flask(__name__)

@app.route('/', methods=['Post', 'Get'])
@app.route('/<json_path>', methods=['Post', 'Get'])
def index(json_path = ""):
    if request.method == 'POST':
        API_URL = request.form['API_URL']
        response_data = requests.get(API_URL).json()
        return render_template('index.html', json_output =  clean_output(response_data)[:-1] )
    elif json_path != "":
        python_code = get_python_code(json_path, "")
        return render_template('index.html', json_output = "", python_code = python_code)
    return render_template('index.html')

def clean_output(response_data, n = 4, python_trace = ""):
    indents = '&nbsp' * n
    cleaned_output = ""
    if type(response_data) == dict:
        cleaned_output = cleaned_output + "{"
        for key in response_data:
            python_trace = python_trace + "key:" +  key + ";" 
            cleaned_output = cleaned_output + "<br>" + indents + key + ": " + clean_output(response_data[key], n *2, python_trace)
            python_trace = ";".join(python_trace[:-1].split(";")[:-1]) + ";" 
            if len(python_trace) == 1:
                python_trace = ""
        cleaned_output = cleaned_output[:-1] + "<br>" + indents[:int(len(indents)/2)] + "},"
    elif type(response_data) == list:
        cleaned_output = cleaned_output + "["
        for index, element in enumerate(response_data):
            python_trace = python_trace + "index:" +  str(index) + ";"
            cleaned_output = cleaned_output + "<br>" + indents  + clean_output(element, n *2, python_trace)
            python_trace = ";".join(python_trace[:-1].split(";")[:-1]) + ";" 
            if len(python_trace) == 1:
                python_trace = ""
        cleaned_output = cleaned_output[:-1] + "<br>" + indents[:int(len(indents)/2)]  + "],"
    else:
        cleaned_output = cleaned_output + f'<a href="/{python_trace[:-1]}">' + str(response_data) + '</a>,'
    return cleaned_output

def get_python_code(json_path, API_URL):
    JSON_path_lst = json_path.split(';')
    python_code = f"API_URL = '{API_URL}' <br> response_data = requests.get(API_URL).json() <br> response_data"
    for key_index in JSON_path_lst:
        index = key_index.split(":")[1]
        if type(index) == int:
            python_code = python_code + f"[{index}]"
        else:
            python_code = python_code + f"['{index}']"
    return python_code
if __name__ == '__main__':
    app.run(debug=True)
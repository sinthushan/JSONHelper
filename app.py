from flask import Flask, render_template, request
import requests
import json
app = Flask(__name__)

@app.route('/', methods=['Post', 'Get'])
def index():
    if request.method == 'POST':
        API_URL = request.form['API_URL']
        print(API_URL)
        response_data = requests.get(API_URL).json()
        return render_template('index.html', task =  clean_output(response_data)[:-1] )
    return render_template('index.html', task = "")

def clean_output(response_data, n = 4, python_trace = ""):
    indents = '&nbsp' * n
    cleaned_output = ""
    if type(response_data) == dict:
        cleaned_output = cleaned_output + "{"
        for key in response_data:
            python_trace = python_trace + "key:" +  key + ";" 
            cleaned_output = cleaned_output + "<br>" + indents + key + ": " + clean_output(response_data[key], n *2, python_trace)
            python_trace = ";".join(python_trace[:-1].split(";").pop())
        cleaned_output = cleaned_output[:-1] + "<br>" + indents[:int(len(indents)/2)] + "},"
    elif type(response_data) == list:
        cleaned_output = cleaned_output + "["
        for index, element in enumerate(response_data):
            python_trace = python_trace + "index:" +  str(index) + ";"
            cleaned_output = cleaned_output + "<br>" + indents  + clean_output(element, n *2, python_trace)
            python_trace = ";".join(python_trace[:-1].split(";").pop())
        cleaned_output = cleaned_output[:-1] + "<br>" + indents[:int(len(indents)/2)]  + "],"
    else:
        cleaned_output = cleaned_output + f'<span id="{python_trace[:-1]}">' + str(response_data) + '</span>,'
    return cleaned_output

if __name__ == '__main__':
    app.run(debug=True)
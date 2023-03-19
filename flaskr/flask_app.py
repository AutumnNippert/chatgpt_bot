from flask import Flask, render_template, request, redirect, url_for
from processing import process_message, get_message_history
import sys

app = Flask(__name__)

@app.route("/")
@app.route("/index")
def hello_world():
    # show index.html
    return render_template('index.html')
    
@app.route("/chat", methods=['POST'])
def chat():
    # get message from index.html
    message = request.form['prompt']
    process_message(message)
    responses = get_message_history()
    #get rid of first message
    responses.pop(0)
    # return response to index.html
    print(responses, file=sys.stderr)
    return render_template('index.html', responses=responses)

app.run(host='0.0.0.0', port=5000)
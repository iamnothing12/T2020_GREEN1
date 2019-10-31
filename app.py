from flask import Flask, render_template, send_from_directory, request, Markup
import requests
import json
import httplib2 as http
import json
import datetime
import pygal

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

app = Flask(__name__, template_folder='Front End')
app.config["DEBUG"] = True



API_IDENTITY = 'Group20'
API_TOKEN = 'd424f61c-a7b0-4809-88e3-161ed390a843'
USERNAME = 'limzeyang'
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json; charset=UTF-8',
    'identity' : API_IDENTITY,
    'token' : API_TOKEN
}

uri = "http://techtrek-api-gateway.ap-southeast-1.elasticbeanstalk.com/"
path = "customers/limzeyang"
target = urlparse(uri+path)
method = 'GET'
body = ''

h = http.Http()
response, content = h.request(
        target.geturl(),
        method,
        body,
        headers)

# assume that content is a json reply
# parse content with the json module
data = json.loads(content)

# print(data)

@app.route('/',methods= ['GET','POST'])
def login():
    return render_template('index.html')

@app.route('/customers',methods=['POST'])
def home(): # need to accept parameters
    text = request.form['username']
    username_field = text
    path = "customers/"+ username_field
    target = urlparse(uri+path)
    response, content = h.request(target.geturl(),method,body,headers)
    customerData = json.loads(content)
    if str(request.form['password']) != 'pass':
        return render_template('index.html')
    if response == 404:
        return render_template('index.html')

    return render_template('login.html',login=customerData)

@app.route('/transaction',methods=['GET'])
def get_transaction():
    # datetime.today().strftime('%Y-%m-%d')
    # print(datetime)

    # date_time_str = '2019-01-29'
    # date_time_obj =

    print('Date:', datetime.datetime.strptime("2013-1-25", '%Y-%m-%d').strftime('%m-/%d-/%y'))
    path = 'transactions/'+ r'74/?from=01-01-2019&to=01-31-2019'
    print (path)
    target = urlparse(uri+path)
    print(target.geturl())
    response, content = h.request(target.geturl(),method,body,headers)
    transactionData = json.loads(content)
    transactionList = {}
    for details in transactionData:
        print(str(details['tag']))
        if details['tag'] in transactionList:
            transactionList[str(details['tag'])] = float(transactionList[str(details['tag'])])+ float(details['amount'])
        else:
            transactionList[str(details['tag'])] = details['amount']
    pie_chart = pygal.Pie()
    pie_chart.title = 'Expenditure based on category'
    for category in transactionList.keys():
        pie_chart.add(category,  float(transactionList[category]))
    # return (pie_chart.render())
    pie_chart = pie_chart.render_data_uri()
    return render_template('transaction.html', chart =pie_chart)



if __name__ == '__main__':
    # init_session()
    app.run()

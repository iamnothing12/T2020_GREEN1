from flask import Flask, render_template, send_from_directory
import requests
import json
import httplib2 as http
import json

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

print(data)

# Custom static data
@app.route("/css/<filename>")
def get_css(filename):
    filename = f"{filename}"
    print (filename)
    return send_from_directory("/Front End/css/", filename=filename, as_attachment=True)
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
    print(content)
    data = json.loads(content)
    return render_template('login.html',login=data)
    # return render_template('login.html', login=json.loads(content))

@app.route('/css')
def css():
    return
# def init_session():
#     r = requests.Session()
#     r.headers.update({'identity':API_IDENTITY,'token':API_TOKEN})
#     r.get('http://techtrek-api-gateway.ap-southeast-1.elasticbeanstalk.com/')



# @app.route('/')
# def login1():
#     r =requests.get("http://techtrek-api-gateway.ap-southeast-1.elasticbeanstalk.com/customers/1")
#     print(r)
#     return render_template('login.html', login=json.loads(r.text))
#     # return render_template('login.html')
# # @app.route('/', methods=['GET', 'POST'])
# # def login():
# #     error = None
# #     if request.method == 'POST':
# #         if request.form['username'] != 'admin' or request.form['password'] != 'admin':
# #             error = 'Invalid Credentials. Please try again.'
# #         else:
# #             return redirect(url_for('home'))
# #     return render_template('login.html', error=error)


# # @app.route('/customers/:<USERNAME>')#,method=['GET'])
# # def homepage(username):
# #     r = requests.Session()
# #     r.headers.update({'identity':API_IDENTITY,'token':API_TOKEN})
# #     r.get('http://techtrek-api-gateway.ap-southeast-1.elasticbeanstalk.com/customers/1')
# #     print (r)
# #     return Response(
# #         r.text,
# #         status=r.status_code,
# #         content_type=r.headers['content-type'],
# #     )
#     # r = requests.get(
#     #   'http://techtrek-api-gateway.ap-southeast-1.elasticbeanstalk.com/')
#     # print(r)
#     # return render_template('login.html', login=json.loads(r.text)['customerId'])

if __name__ == '__main__':
    # init_session()
    app.run()
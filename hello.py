from flask import Flask, render_template
import json
from database_interface import pull_names, returnConn
from flask import jsonify

app = Flask(__name__)

# @app.route('/s')
# def home():
#     return render_template('home.html')

@app.route('/')
def summary():
    lists = newperson()
    return lists[0]

def newperson(pull_names_list = pull_names()):

    json_items = []
    for item in pull_names_list:
        uuid = item[0]
        name = item[1]
        school = item[2]
        email = item[3]
        password = item[4]
        role = item[5]
        rep = item[6]
        classes = list(item[7].split('-'))

        value = {
           "name": name,
           "uuid": uuid,
           "school": school,
           "email": email,
           "password": password,
           "role": role,
           "rep": rep,
           "classes": classes
        }

        json_items.append(json.dumps(value))
    return json_items

if __name__ == '__main__':
    app.run()

    
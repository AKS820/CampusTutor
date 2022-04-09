from flask import Flask, render_template, url_for
import json
from database_interface import pull_names, returnConn

app = Flask(__name__)

@app.route('/')
def general():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

def newperson(pull_names_list = pull_names()):

    items = []
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
           "name": str(name),
           "uuid": str(uuid),
           "school": str(school),
           "email": str(email),
           "password": str(password),
           "role": str(role),
           "rep": str(rep),
           "classes": str(classes)
        }

        items.append(value)
    return items



@app.route('/findtutors')
def finder():
    return render_template('finder.html', posts = newperson())

if __name__ == '__main__':
    app.run()

    
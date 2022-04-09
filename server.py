import json
from os import environ as env
from urllib.parse import quote_plus, urlencode

from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, session, url_for, request

from database_interface import pull_names, createUser, create_table, getTutors
from flask import jsonify

from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from twilio.twiml.messaging_response import MessagingResponse

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")


oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration',
)

account_sid = "ACd764836049147497da855308896f8322"
auth_token = "59efb831f503f55c554d8e59fb5b3427"
client = Client(account_sid, auth_token)


@app.route("/")
def home():
    create_table()
    if(session):
        email = session.get("user").get("userinfo").get("email")
        user = getUserData(newperson(), email)
        if(user):
            school = json.loads(user).get("school")
            role = json.loads(user).get("role")
            classes = json.loads(user).get("classes")
            return render_template(
                "home.html",
                session=session.get("user"),
                school = school,
                role = role,
                classes = classes,
                pretty=json.dumps(session.get("user"), indent=4),
            )
        else:
            return render_template("signup.html", email=email)
    else:
        return render_template("login.html")
    
def getUserData(users, email):
    for user in users:
        juser = json.loads(user)
        if(juser["email"]==email):
            return user

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

@app.route("/createUser", methods = ['POST', 'GET'])
def data():
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        form_data = request.form
        createUser(form_data)
        return redirect("/logout")
        
@app.route("/getTutors", methods = ['POST', 'GET'])
def tutorData():
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        form_data = request.form
        tutors = newperson(getTutors(form_data))
        newtutors = []
        for tutor in tutors:
            newtutors.append(json.loads(tutor))
        return render_template("TutorSelector.html", tutors = newtutors)

@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")


@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://"
        + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

@app.route("/sms")
def sms():
    name = session.get("user").get("userinfo").get("name")
    phoneNumber = session.get("user").get("userinfo").get("number")

    call = client.messages.create(
        body="{} has expressed interest in you. Would you like to visit their profile? (YES/NO)".format(name),
        #to = "{}".format(phoneNumber),
        to = "+12485335849",
        from_ = "+12182198066")
    msg = incoming_sms()

def incoming_sms():
    body = request.values.get('Body',None)
    resp = MessagingResponse()

    name = session.get("user").get("userinfo").get("name")
    school = session.get("user").get("userinfo").get("school")
    classes = session.get("user").get("userinfo").get("classes")
    rep = session.get("user").get("userinfo").get("rep")

    if body.lower() == 'yes':
        resp.message("{} is a student at {} and is in these classes: {}. This is their description: {}. Check them out on our website for more information".format(name,school,*classes, rep))
    elif body.lower() == 'no':
        resp.message("Request Ignored")
    return str(resp)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=env.get("PORT", 3000))
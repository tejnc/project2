import os
from typing_extensions import Required
from dotenv import load_dotenv
from flask_mongoengine import MongoEngine
from flask import Flask, jsonify, request

app = Flask(__name__)
load_dotenv()


app.config['MONGODB_SETTINGS']={
    'db':'mongoEngine_db',
    'host':os.environ["MONGO_URI"]
}
db = MongoEngine()
db.init_app(app)


class Users(db.Document):
    name = db.StringField()
    email = db.EmailField()
    password = db.StringField()



@app.route('/register',methods=["POST"])
def register_user():
    """"
        User Registration
    """
    if request.method=="POST":
        _json = request.json
        _name = _json["name"]
        _email = _json["email"]
        _password = _json["password"]

        _user = Users(name=_name, email=_email,password=_password)
        _user.save()

if __name__=="__main__":
    app.run(debug=True)

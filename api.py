import os
import jwt
import time
import datetime
from dotenv import load_dotenv
from bson.json_util import default, dumps
from flask_mongoengine import MongoEngine
from flask import Flask, json, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash

from utils.user_fun import get_user_by_id


app = Flask(__name__)
load_dotenv()


app.config['MONGODB_SETTINGS']={
    'db':'mongoEngine_db',
    'host':os.environ["MONGO_URI"]
}
db = MongoEngine()
db.init_app(app)


class Users(db.Document):
    name = db.StringField(required=True)
    gender = db.StringField()
    phone_number=db.StringField()
    address=db.DictField()
    email = db.EmailField(required=True,unique=True)
    password = db.StringField(required=True)
    created = db.DateTimeField(default=datetime.datetime.utcnow)

    def to_json(self):
        return {
            "name":self.name,
            "gender":self.gender,
            "phone_number": self.phone_number,
            "address":self.address,
            "email":self.email
        }


@app.route('/register',methods=["POST"])
def register_user():
    """"
        User Registration
    """
    if request.method=="POST":
        _json = request.json
        _name = _json["name"]
        _gender = _json["gender"]
        _phone_number = _json["phone_number"]
        _address = {
            "province":_json["province"],
            "district":_json["district"],
            "town":_json["town"]
        }
        _email = _json["email"]
        _password = _json["password"]


        _hashed_password = generate_password_hash(_password)
        _user = Users(
            name=_name, 
            gender=_gender, 
            phone_number=_phone_number,
            address=_address,
            email=_email,
            password=_hashed_password)
        _user.save()
        resp = jsonify("User added successfully.")
        resp.status_code = 200
        return resp
    
    else:
        return not_found()

@app.errorhandler(404)
def not_found(error=None):
    message = {
        "status": 404,
        "message": "Not found" + request.url
    }

    resp = jsonify(message)
    resp.status_code = 404
    return resp



@app.route("/login", methods=["POST"])
def login_user():
    """
        User login
    """
    _json = request.json
    _email = _json["email"]
    _password = _json["password"]

    logged_user = Users.objects.get(email=_email)

    if logged_user:
        if check_password_hash(logged_user["password"],_password):
            """
                checking password and implementing jwt tokens
            """
            token = jwt.encode(
                {
                    "id": logged_user["name"],
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=45),
                },
                os.environ["KEY"]
                
            )

            resp = jsonify({
                "message":"User logged in successfully.",
                "token":token
            })
            resp.status_code = 200
            return resp
    else:
        resp = jsonify("user not found!")
        return resp

# protected api
@app.route("/users")
def users_list():
    """ 
        It shows the list of users.
    """
    
    users = []
    current_time = time.time()
    exp_time = get_user_by_id(request.headers)["exp"]
    print(exp_time,current_time)

    if exp_time > current_time:
        for user in Users.objects.exclude("password"):
            users.append(user.to_json())
        return jsonify(users)
        

if __name__=="__main__":
    app.run(debug=True)

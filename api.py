from flask import Flask, jsonify, request
from flask_mongoengine import MongoEngine
from dotenv import load_dotenv


app = Flask(__name__)
load_dotenv()


app.config['MONGODB_SETTINGS']={
    'db':'mongoEngine_db',
    'host':'mongodb+srv://test:test@cluster0.x25kn.mongodb.net/mongoEngine_db?retryWrites=true&w=majority'
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

from app import db
from werkzeug.security import check_password_hash, generate_password_hash

class User(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    phone_number = db.Column(db.String(12), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
   

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class Chat(db.Model):
    id= db.Column(db.Integer, unique=True,primary_key=True)
    username = db.Column(db.Integer, nullable=False)
    user = db.Column(db.TEXT, nullable=False)
    bot = db.Column(db.TEXT, nullable=False)
    
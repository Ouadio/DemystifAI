
from web_apps import db, bcrypt, login_manager
from flask_login import UserMixin


################      CREATE MODELS      #####################

@login_manager.user_loader
def load_user(user_id):
    return(User.query.get(user_id))

#Double inheritence to use the UserMixin attributes & Methods
class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    pseudo = db.Column(db.String(10), unique = True)
    email = db.Column(db.String(20), unique = True)
    password_hash = db.Column(db.String(150))
    fullname = db.Column(db.Text)
    birthdate = db.Column(db.Text)
    
    def __init__(self, pseudo, email, fullname, birthdate, password):
        self.pseudo = pseudo
        self.email= email
        self.fullname = fullname
        self.birthdate = birthdate
        self.password_hash = bcrypt.generate_password_hash(password)
    
    def check_password(self, password):
        return(bcrypt.check_password_hash(self.password_hash, password))
    
    def __repr__(self):
        return(f"Your pseudo is {self.pseudo} and your signing email is {self.email}")
        
        


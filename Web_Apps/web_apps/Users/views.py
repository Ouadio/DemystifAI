
#From the app
from web_apps import  db, bcrypt
#Flask basics
from flask import ( render_template, redirect, url_for, flash, Blueprint, request)  
#Models
from web_apps.models import User                 
#Forms 
from web_apps.Users.forms import signInForm, signUpForm, deleteForm, modifyForm

#User Auth
from flask_login import login_user, login_required, logout_user
    
##Blueprint Setup

users_blueprints = Blueprint('users', __name__, template_folder='templates/Users')


####################   VIEW FUNCTIONS     ##########################
        
        
#@app.route('/', methods = ['GET', 'POST'])
@users_blueprints.route('/', methods = ['GET','POST'])
def acceuil():    
    return(render_template("welcome.html"))
    
#@app.route('/signup', methods = ['GET','POST'])
@users_blueprints.route('/signup', methods = ['GET','POST'])
def signup():
    signup_form = signUpForm()
    
    if signup_form.validate_on_submit():
        name = signup_form.name.data
        email = signup_form.email.data
        pseudo = signup_form.pseudo.data
        birthdate = signup_form.birthdate.data
        password = signup_form.password.data
        
        myUser = User(pseudo=pseudo,email=email, fullname=name, 
                      birthdate=birthdate, password = password)
        
        user_by_email = User.query.filter_by(email=email).first()
        user_by_pseudo = User.query.filter_by(pseudo=pseudo).first()
        
        if user_by_email is None and user_by_pseudo is None :
            
        
            db.session.add(myUser)
            db.session.commit()
            return(redirect(url_for('users.signin')))
        else:
            flash("The email and/or pseudo provided already exist(s) !")
    
    return(render_template('signup.html', signup_form= signup_form))
    



#@app.route('/signin', methods = ['GET','POST'])
@users_blueprints.route('/signin', methods = ['GET','POST'])
def signin():
    signin_form = signInForm()    
    
    if signin_form.validate_on_submit():
        email = signin_form.email.data
        password = signin_form.password.data 
        
        myUser = User.query.filter_by(email=email).first()
        
        
        if myUser is None:
            flash("The email provided doesn't correspond to any user !")
            return(redirect(url_for('users.signin')))
            
        if myUser.check_password(password):
            login_user(myUser)
            flash(f"Hi again {myUser.pseudo}! Welcome Back")
            #This next refers to the page the user is trying to access
            #for instance, if he's trying to go to his avatar, and he's not logged in 
            #this next will save that request and will redirect him there once logged.
            next = request.args.get("next")
            if next==None or not next[0]=='/':
                next = url_for('users.avatar', myPseudo = myUser.pseudo)
            
            return(redirect(next))
        else:
            flash(f"The password you intered is invalid. Try again. ")


    return(render_template("signin.html", signin_form = signin_form))
        

@users_blueprints.route('/avatar/<myPseudo>', methods = ['GET','POST'])
@login_required
def avatar(myPseudo):
    return(render_template('avatar.html'))
    
    
@users_blueprints.route('/avatar/modify/<myPseudo>', methods = ['GET','POST'])
@login_required
def modifying(myPseudo):
    user = User.query.filter_by(pseudo=myPseudo).first()
    #Modify
    modify_form = modifyForm()
    if modify_form.validate_on_submit():
        user.pseudo = modify_form.pseudo.data
        user.password_hash = bcrypt.generate_password_hash(modify_form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f"The modification succeeded, your new pseudo is {user.pseudo} !")
        return(redirect(url_for('users.avatar',myPseudo = myPseudo )))
    #Delete
    delete_form = deleteForm()
    if delete_form.validate_on_submit():
        db.session.delete(user)
        db.session.commit()
        return(redirect(url_for('users.acceuil')))
        
    return(render_template("modifying.html",modify_form=modify_form, delete_form=delete_form ))
    

@users_blueprints.route('/avatar/logout', methods = ['GET','POST'])
@login_required
def logout():
    logout_user()
    #flash("See you soon. Bye.")
    return(redirect(url_for('users.acceuil')))








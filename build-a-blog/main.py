from flask import Flask, request, redirect, render_template, session, flash
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import cgi
import os

#Note: the connection string after :// contains the following info:
#
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build-a-blog@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'hoursewhisperralphsoupgoose'

"""
class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    entries = db.relationship('Blog', backref='author_id')

    def __init__(self, email, password):
        self.email = email
        self.password = password
"""

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    blog_title = db.Column(db.String(250))
    body = db.Column(db.String(10000))
    blog_date = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    post_deleted = db.Column(db.Boolean)
    #author_id = db.Column(db.Integer, db.ForeignKey('user.id'))    
    

    def __init__(self, blog_title, body, blog_date, post_deleted): #author
        self.blog_title = blog_title
        self.body = body
        #self.author = author
        self.post_deleted = False       
        self.blog_date = blog_date


@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        blog_title = request.form['title']
        body = request.form['n_blog']
        new_body = blog(body)
        new_title = blog(blog_title)
        db.session.add(new_blog)
        db.session.add(new_title)
        db.session.commit()

    #titles = blog.query.filter_by(post_deleted=False).all()
    return render_template('newpost.html',title="Blog posts", new_body = new_body, new_title = new_title )

@app.route('/blog', methods=['POST', 'GET'])
def blog():
    blogs= Blog.query.filter_by(deleted_post=False).all()
    return render_template('blog.html', blogs=blogs)


@app.route('/delete-entry', methods=['POST'])
def delete_entry():

    entry_id = int(request.form['entry-id'])
    body = Blog.query.get(entry_id)
    blog_title = Blog.query.get(entry_id)

    db.session.delete(blog_title)
    db.session.delete(body)
    db.session.commit()

    return redirect('/')

@app.before_request
def require_login():
    allowed_routes = ['newpost']
    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect('/newpost')

#
"""
@app.route('/login', methods=['POST','GET'])
def login():

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            flash("You're logged in")
            session['email'] = email
            #todo - "remember" that the user has logged in"
            return redirect('/')
        else:
            #tell the user why the login failed
            flash("login failed, try again")
            return redirect('/login')   
    return render_template('login.html', title="Login - !")

@app.route('/logout', methods=['POST', 'GET'])
def logout():
    del session['email']
    return redirect('/')    


@app.route('/register', methods=['POST','GET'])
def register_user(): 
    if request.method == 'GET':
        return render_template('register.html')
    else:
        email = request.form('email')
        password = request.form('password')
        pass_verify = request.form('pass_verify')
        if not validate(email, password, pass_verify):
            flash("Invalid Email")
            return redirect('/register')

        new_user = User(email, password)
        #we have two different types of sessions running
        #one between the db and the website and the other between the website and the user
        db.session.add(new_user)    
        db.session.commit()
        session['email'] = email
    return render_template('register.html', title="Register to build a blog")


def validate(email, password, pass_verify):
    
    
    #error messages
    
    p_error = ""
    p2_error = ""
    email_error = ""
    
    # Validate Username
    if email == password1:
        email_error = "your username and password may not be the same"
        p_error= "your username and password may not be the same"

    
        
    if not length(email):
        email_error = "Your username is too long or too short"

    if  not email.isalnum():
        usr_error = "You have invalid characters in your username"

    if not space(email):
        usr_error = "you have spaces in your username"

    if not has_val(email):
        usr_error = "The username field cannot be blank :}"

    if has_val(email):
        if not email_chk(email):
            email_error = "this is not a valid email address"
    else:
        email_error = ""     
    # Validate Password
    

    if password1 != password2:
        p_error = "Your passwords must match"
        p2_error = "Your passwords must match"

    if not space(password1):
        p_error = "passwords cannot have spaces"
   
    if not length(password1):
        p_error = "password length outside of range (3 < password < 20)"
    

    if not password1.isalnum():
        p_error = "you have unaccepable symbols in your password"

    if not has_val(password1) or not has_val(password2):
        p_error ="You have left a necessary field blank"    


    #TEST RETURN
    if p_error == "" and p2_error == "" and email_error == "":
        return True
    else:
        return (False, p_error,
         usr_name, 
         email_error,
         p2_error)    


def has_val(text):
    if text == "" or text.strip() == "":
        return False
    else:
        return True    

def space(text):
    sp = " "
    if sp not in text:
        return True
    else:
        return False

def length(text):
    if len(text) >= 3 and len(text) <= 20:
        return True
    else:
        return False

def email_chk(text):
    if "@" in text and "." in text:
        return True
    else:
        return False     
"""



if __name__ == '__main__':
    app.run()

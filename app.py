from flask import Flask,render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField
from wtforms.validators import InputRequired,Email,Length
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['SECRET_KEY']='thisissecret'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:////C/Python34/emaildb.sqlite'
Bootstrap(app)
db=SQLAlchemy(app)

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(15),unique=True)
    email=db.Column(db.String(50),unique=True)
    password=db.Column(db.String(80))
    

class LoginForm(FlaskForm):
    username=StringField('username',validators=[InputRequired(), Length(min=4,max=15)])
    password=PasswordField('password',validators=[InputRequired(),Length(min=8,max=80)])
    remember=BooleanField('remember')
class RegisterForm(FlaskForm):
    email=StringField('email',validators=[InputRequired(),Email(message='Invalid email'),Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login',methods=['POST','GET'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        return ' ' + form.username.data
    return render_template('login.html',form=form)

@app.route('/signup',methods=['POST','GET'])
def signup():
    form=RegisterForm()
    if form.validate_on_submit():
        return ' '+ form.email.data
    return render_template('signup.html',form=form)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__=="__main__":
    app.run(debug=True)

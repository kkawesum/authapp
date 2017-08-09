from flask import Flask,render_template,redirect,url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField
from wtforms.validators import InputRequired,Email,Length
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_required,login_user,logout_user,fresh_login_required,LoginManager,current_user,UserMixin

app=Flask(__name__)
db_path = os.path.join(os.path.dirname(__file__), 'app.db')
db_uri = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SECRET_KEY']='thisissecret'
Bootstrap(app)
db=SQLAlchemy(app)
login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'


class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(15),unique=True)
    email=db.Column(db.String(50),unique=True)
    password=db.Column(db.String(80))
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


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
        user=User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password,form.password.data):
                login_user(user,remember=form.remember.data)
                return redirect(url_for('dashboard'))
        return 'Invalid credentials '
    return render_template('login.html',form=form)

@app.route('/signup',methods=['POST','GET'])
def signup():
    form=RegisterForm()
    if form.validate_on_submit():
        hashed_password=generate_password_hash(form.password.data,method='sha256')

        new_user=User(username=form.username.data,email=form.email.data,password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return 'new user created'

    return render_template('signup.html',form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__=="__main__":
    app.run(debug=True)

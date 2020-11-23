from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import UserForm, LoginForm, FeedbackForm
from sqlalchemy.exc import IntegrityError
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL',"postgres:///feedback_db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY','iamsosecret123')
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)

toolbar = DebugToolbarExtension(app)

@app.route('/')
def viewing_page():
    return redirect('/register')

@app.route('/register', methods=['GET','POST'])
def register_user():
    form=UserForm()
    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data
        email=form.email.data
        first_name=form.first_name.data
        last_name=form.last_name.data
        pwd=User.register(username,password)
        new_user=User(username=username,password=pwd,email=email,
                    first_name=first_name,last_name=last_name)
        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username taken. Please pick another one')
            return render_template('register.html',form=form)
        session['user_name']=new_user.username
        flash('Welcome! Your Account Successfully Created!', "success")
        return redirect(f'/users/{new_user.username}')
    return render_template('register.html',form=form)

@app.route('/users/<username>')
def feedbacks(username):
    if 'user_name' not in session:
        flash('First you must login!',"danger")
        return redirect('/register')
    user=User.query.get_or_404(username)
    feedbacks=Feedback.query.all()
    return render_template('feedbacks.html',user=user,feedbacks=feedbacks)

@app.route('/login', methods=['GET','POST'])
def login_user():
    form=LoginForm()
    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data
        user=User.authenticate(username,password)
        if user:
            flash(f'Welcome back, {user.username}','success')
            session['user_name']=user.username
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors=['Invalid Username/password']
    return render_template('login.html',form=form)

@app.route('/logout')
def logout_user():
    session.pop('user_name')
    flash('Goodbye!','info')
    return redirect('/')

@app.route('/users/<username>/feedback/add', methods=['GET','POST'])
def add_feedback(username):
    if 'user_name' not in session:
        flash('You must login first','danger')
        return redirect('/login')
    form=FeedbackForm()
    if form.validate_on_submit():
        title=form.title.data
        content=form.content.data
        new_feedback=Feedback(title=title,content=content,username=username)
        db.session.add(new_feedback)
        db.session.commit()
        flash('Feedback successfully Added','info')
        return redirect(f'/users/{username}')
    return render_template('feedback_form.html',form=form)

@app.route('/users/<username>/delete',methods=['POST'])
def delete_user(username):
    if 'user_name' not in session:
        flash('You must login first','danger')
        return redirect('/login')
    user=User.query.get_or_404(username)
    if user.username==session['user_name']:
        db.session.delete(user)
        db.session.commit()
        session.pop('user_name')
        flash("Account deleted!",'success')
        return redirect('/')
    flash("You don't have permission to delete this account")
    return redirect('/register')

@app.route('/feedback/<int:id>/update', methods=['GET','POST'])
def edit_feedback(id):
    if 'user_name' not in session:
        flash('You must login first','danger')
        return redirect('/login')
    feedback=Feedback.query.get_or_404(id)
    form=FeedbackForm(obj=feedback)
    if feedback.username==session['user_name']:
        if form.validate_on_submit():
            feedback.title=form.title.data
            feedback.content=form.content.data
            db.session.commit()
            flash("Feedback Updated!",'success')
            return redirect(f'/users/{session["user_name"]}')
        return render_template('feedback_update.html',form=form)
    flash("You don't have permission to edit this feedback",'danger')
    return redirect(f'/users/{session["user_name"]}')

@app.route('/feedback/<int:id>/delete', methods=['POST'])
def delete_feedback(id):
    if 'user_name' not in session:
        flash('You must login first','danger')
        return redirect('/login')
    feedback=Feedback.query.get_or_404(id)
    if feedback.username==session['user_name']:
        db.session.delete(feedback)
        db.session.commit()
        flash("Feedback deleted!",'info')
        return redirect(f'/users/{session["user_name"]}')
    flash("You don't have permission to delete this feedback",'danger')
    return redirect(f'/users/{session["user_name"]}')

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404
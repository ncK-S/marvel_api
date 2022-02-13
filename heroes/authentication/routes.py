#package imports

from flask import Blueprint, flash, redirect, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required

# project file imports
from  heroes.forms import UserLoginForm
from heroes.models import User, db, check_password_hash

auth = Blueprint('auth', __name__, template_folder = 'auth_templates')

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = UserLoginForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email, password)

            # add user to db
            user = User(email, password = password)
            db.session.add(user)
            db.session.commit()

            flash(f'Congratulations! You have successfully created an account for {email}.','user-created')
            return redirect(url_for('auth.signin'))

    except:
        raise Exception('Ivalid Form Data: Please check your credentials')


    return render_template('signup.html', form=form)

@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    form = UserLoginForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email, password)

            #Query user table for users with this info
            logged_user = User.query.filter(User.email == email).first()
            # check if login credentials  == valid
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                flash('you were successfully logged in')
                return redirect(url_for('site.profile'))
                
            else:
                flash('Your email or password is incorrect.', 'auth-failed')
                return redirect(url_for('auth.signin'))


            

    except:
        raise Exception('Ivalid Form Data: Please check your credentials')
    
    return render_template('signin.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('site.home'))

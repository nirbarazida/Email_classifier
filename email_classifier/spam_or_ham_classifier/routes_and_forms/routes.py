from flask import render_template, url_for, flash, redirect, request, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
from email_classifier.spam_or_ham_classifier.routes_and_forms._general_functions import statistics
from email_classifier.spam_or_ham_classifier.classification_model import predict_SOH
from email_classifier.spam_or_ham_classifier.routes_and_forms.forms import RegistrationForm, LoginForm, ClassificationForm
from email_classifier.spam_or_ham_classifier import app, bcrypt, db
from email_classifier.spam_or_ham_classifier.web_database.ORM import UserTable, EmailClassifiedTable


@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    """
    Home page:
     if the user is not connected will show LoginForm else application statistics
     after login will redirect back to home page
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = UserTable.query.filter_by(username=form.username.data).first()

        # passwords in the database are encrypted - when trying to log check_password_hash
        # compares the database password and the user input
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'Login successfully', 'success')
            return redirect(url_for('home'))
        else:
            flash(f'Login unsuccessfully for {form.username.data}', 'danger')

            # statistics() returns all website current statistics
    return render_template('home.html', form=form, statistics=statistics())


@app.route("/classifier", methods=['GET', 'POST'])
# @login_required # TODO: how to connect as user using request??
# todo: add 'spam_or_ham_db' to git ignore
def classifier():
    """
    Email classifier can be used with 3 methodes:
     1. singel request using param: returens a string - 'Spam' / 'Ham'
     2. multi requests using json file: returns json file with the label for evey email and as list
                                        under {labels: ['Spam','Spam', 'Ham','Spam','Ham'..]
     3. using user interface ClassificationForm :  flash 'Spam' / 'Ham'
                                                add the labeled email to the user database of libeled emails.
                                                will show all libeled emails. when logged-in under /classifier.html


    """
    # Validate the request body contains JSON - works as API
    if request.is_json:

        # Parse the JSON into a Python dictionary
        req = request.get_json()

        # Create a prediction json file
        y_pred = {'label': []}

        # phrs all email in json file and make a prediction
        for index in req:
            y_pred[index] = {}
            y_pred[index]['content'] = req[index]['content']
            y_pred[index]['label'] = 'Ham' if predict_SOH(req[index]['content']) == 0 else 'Spam'
            y_pred['label'].append(y_pred[index]['label'])
        return jsonify(y_pred)

    # API single prediction
    elif request.args.get('content'):
        content = str(request.args.get('content'))
        return predict_SOH(content)

    # using application form
    else:
        form = ClassificationForm()

        # todo : #1 un-mute after fixing login problem

        # all the emails that the current_user have classified - will show them in this page.
        # page = request.args.get('page', 1, type=int)
        # classified = EmailClassifiedTable.query.filter_by(user=current_user).order_by(
        #     EmailClassifiedTable.data_classified.desc()).paginate(page=page, per_page=5)

        # todo : #1 delete after fixing login problem
        classified = None
        user = UserTable.query.filter_by(username='admin').first()  # current_user

        if form.validate_on_submit():
            # make a prediction to the form input email
            label = predict_SOH(form.email_cont.data)

            # todo : #1 after fixing login problem - change user to current_user
            # create EmailClassifiedTable instance and commite to the database
            new_classification = EmailClassifiedTable(email_title=form.email_title.data,
                                                      email_content=form.email_cont.data,
                                                      user=user, label=label,
                                                      data_classified=datetime.now())
            db.session.add(new_classification)
            db.session.commit()
            flash(f'The email is : Ham', 'success') if label == 'Ham' else flash(f'The email is : Spam', 'danger')

            return redirect(url_for('classifier'))
        return render_template('classifier.html', title='Classifier', form=form, classified=classified,
                               statistics=statistics())


@app.route("/register", methods=['GET', 'POST'])
def register():
    """
     registration page for new users
    """
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        # encrypt user password before commit it the database
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = UserTable(username=form.username.data, password=hashed_password, member_since=datetime.now(),
                         email_address=form.email.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account has been created', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Registration', form=form, statistics=statistics())


@app.route("/login", methods=['GET', 'POST'])
def login_func():
    """
    User login page
    """
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = UserTable.query.filter_by(username=form.username.data).first()

        # passwords in the database are encrypted - when trying to log check_password_hash
        # compares the database password and the user input
        if user and bcrypt.check_password_hash(user.password, form.password.data):

            login_user(user, remember=form.remember.data)
            flash(f'Login successfully', 'success')
            # if  login message was thrown - will re-direct the user (after login) to asked page
            next_page = request.args.get('next')
            return redirect(url_for(next_page.strip('/'))) if next_page else redirect(url_for('home'))
        else:
            flash(f'Login unsuccessfully for {form.username.data}', 'danger')
    return render_template('login.html', title='Login', form=form, statistics=statistics())


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/classifier/<int:clf_email_id>", methods=['GET', 'POST'])
@login_required
def classified_email(clf_email_id):
    """
    the page of the classified email
    :param clf_email_id: the email id that the user clicked on to view in full page
    """
    clf_email = EmailClassifiedTable.query.get_or_404(clf_email_id)
    return render_template('classified_email.html', title='classified email', clf_email=clf_email,
                           statistics=statistics())

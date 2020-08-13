from flask import render_template, url_for, flash, redirect, request, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
from spam_or_ham_classifier.routes_and_forms._general_functions import statistics
from spam_or_ham_classifier.classification_model import predict_SOH
from spam_or_ham_classifier.routes_and_forms.forms import RegistrationForm, LoginForm, ClassificationForm
from spam_or_ham_classifier import app, bcrypt, db
from spam_or_ham_classifier.web_database.ORM import UserTable, EmailClassifiedTable


@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    form = LoginForm()
    if form.validate_on_submit():
        user = UserTable.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'Login successfully', 'success')
            return redirect(url_for('home'))
        else:
            flash(f'Login unsuccessfully for {form.username.data}', 'danger')
    return render_template('home.html', form=form, statistics=statistics())


@app.route("/classifier", methods=['GET', 'POST'])
# @login_required # TODO: how to connect as user using request??
def classifier():
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
    try:
        content = str(request.args.get('content'))
        return 'Ham' if predict_SOH(content) == 0 else 'Spam'

    # using application form
    except:
        form = ClassificationForm()
        page = request.args.get('page', 1, type=int)
        classified = EmailClassifiedTable.query.filter_by(user=current_user).order_by(
            EmailClassifiedTable.data_classified.desc()).paginate(page=page, per_page=5)
        if form.validate_on_submit():
            label = 'Ham' if predict_SOH(form.email_cont.data) == 0 else 'Spam'
            new_classification = EmailClassifiedTable(email_title=form.email_title.data,
                                                      email_content=form.email_cont.data,
                                                      user=current_user, label=label,
                                                      data_classified=datetime.now())
            db.session.add(new_classification)
            db.session.commit()
            flash(f'The email is : Ham', 'success') if label == 'Ham' else flash(f'The email is : Spam', 'danger')

            return redirect(url_for('classifier'))
        return render_template('classifier.html', title='Classifier', form=form, classified=classified,
                               statistics=statistics())


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
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
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = UserTable.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'Login successfully', 'success')
            # if  login message was throw will re direct after login to same web page
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
    clf_email = EmailClassifiedTable.query.get_or_404(clf_email_id)
    return render_template('classified_email.html', title='classified email', clf_email=clf_email,
                           statistics=statistics())

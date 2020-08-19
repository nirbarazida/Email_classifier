from email_classifier.spam_or_ham_classifier.routes_and_forms.routes import app
import os

if __name__ == '__main__':

    # Heroku provides environment variable 'PORT' that should be listened on by Flask
    port = int(os.environ.get('PORT'))

    if port:
        # 'PORT' variable exists - running on Heroku, listen on external IP and on given by Heroku port
        app.run(host='0.0.0.0', port=port)
    else:
        # 'PORT' variable doesn't exist, running not on Heroku, presumabely running locally, run with default
        #   values for Flask (listening only on localhost on default Flask port)
        app.run(debug=True)


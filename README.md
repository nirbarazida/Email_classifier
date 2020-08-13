# Email Classifier
### Random forest classifier for spam or ham emails (deploied on linode sever)

This Classifier was created as part of a home assignment at the 'Israeli Tech Challenge' Bootcamp.\
The main purpose of this classifier is to determine if an email is spam or ham.

The model predictions are based on the 'Enron' database provided by the NLP group at the Athens University of Economics and Business [AUEB](http://nlp.cs.aueb.gr/software.html) .\
I've used this data to train a spam filter, using a processed version of the Enron dataset including labels for "ham" (non-spam) and spam emails.\
I this case I've used the AUEB predictions as the true label of the data and classified the data for ham or spam myself.

First I've used '**CountVectorizer**' from '**Sklearn**' to create Vectorize the words in the dataset into 500 different features that were created from 1-2 words.\
After trying different prediction models the one how to produce the best score with 97% of precision is '**Random Forest Classifier**'.\
To prefect the classifier I have used GridSearchCV from 'Sklearn' to find the best parameters on the train dataset.\
Then, to deploy the Classifier to an online server I have used the 'Pickle' package to 'zip' them.\
When the website is activated the models are loaded and can be used to create prediction in last than 1 sec!

Moreover, I have created an **SQLite** database for user accounts, classified email archives, and API statistics.\
For that, I have mainly used 'flask' extensions

I have deployed the model to a Linux server provided by 'Linode'.\
To do so I have used '**Nginx**', '**Gunicorn**' ,'**flask**' extensions and **bash scripting**

Hope you enjoy my website and wish you good luck,

yours,
Nir Barazida

# Website Screenshots

- Homepage for visitors:\
![screenshot_1](https://github.com/nirbarazida/email_classifier/blob/master/documentation/screenshot_1.png)

- Homepage for users:\
![screenshot_2](https://github.com/nirbarazida/email_classifier/blob/master/documentation/screenshot_2.png)

- Classifier:\
![screenshot_3](https://github.com/nirbarazida/email_classifier/blob/master/documentation/screenshot_3.png)

#Sources:
- [Corey Schafer tutorial](https://www.youtube.com/watch?v=MwZwr5Tvyxo&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH&index=1)
- [Flask documentation](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
- [linode server provider](https://cloud.linode.com/)
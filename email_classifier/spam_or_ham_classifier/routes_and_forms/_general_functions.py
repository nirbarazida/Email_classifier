from email_classifier.spam_or_ham_classifier.web_database.ORM import UserTable, EmailClassifiedTable

def statistics():
    """
     query the database of all current statistics that are displayed for the users
     on the right top bar.
     :return dict with all the relevant values from the database
    """
    return {'registered_users':UserTable.query.count(),
            'emails_classified':EmailClassifiedTable.query.count(),
            'emails_ham':EmailClassifiedTable.query.filter_by(label='Ham').count(),
            'emails_spam':EmailClassifiedTable.query.filter_by(label='Spam').count(),
            'last_classified':EmailClassifiedTable.query.order_by(
                                EmailClassifiedTable.data_classified.desc()).first()}
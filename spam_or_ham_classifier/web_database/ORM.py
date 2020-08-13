from spam_or_ham_classifier import db
from spam_or_ham_classifier import login_manager


@login_manager.user_loader
def load_user(user_id):
    return UserTable.query.get(int(user_id))


class UserTable(db.Model):
    """
    stores all the user that was register to the website.
    relationship:
        Email - one to many
    """

    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), nullable=False, unique=True)
    password = db.Column(db.String(500), nullable=False)
    member_since = db.Column(db.DateTime())
    email_address = db.Column(db.String(30), nullable=False, unique=True)
    email = db.relationship("EmailClassifiedTable", backref="user", lazy=True)

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return str(self.id)
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')

class EmailClassifiedTable(db.Model):
    """
    store all the new e-mail prediction of the model.
    relationship:
        UserTable - one to many

    """
    __tablename__ = 'email'
    id = db.Column(db.Integer(), primary_key=True)
    label = db.Column(db.String(10), nullable=False, unique=False)
    email_title = db.Column(db.String(16000000), nullable=True)
    email_content = db.Column(db.String(16000000), nullable=False)
    data_classified = db.Column(db.DateTime())
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)

db.create_all()
import pickle
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import string

# open pickled vectorizer model - create 500 features of words based on the model_fit parameters
filename_vectorizer_model_for_SOH = 'vectorizer_model_for_SOH.pkl'
loaded_vectorizer_model_for_SOH = pickle.load(open(filename_vectorizer_model_for_SOH, 'rb'))

# open pickled Random Forest Model model
filename_rfc_model_for_SOH = 'rfc_model_for_SOH.pkl'
loaded_rfc_model_for_SOH = pickle.load(open(filename_rfc_model_for_SOH, 'rb'))

# Create new model based on the feature_names of the trained model
new_vectorizer_model = CountVectorizer(vocabulary=loaded_vectorizer_model_for_SOH.get_feature_names(),
                                       encoding='utf-8', decode_error='ignore', stop_words='english',
                                       analyzer='word', ngram_range=(1, 2), max_features=500)


def predict_SOH(email):
    """
    :param email: string
                email with noise such \n, $ etc.
    Work flow:
        1. strip the model from nose charecters
        2. create a vectorized object where the features are the RFC tarin model.
        3. create a prediction using  Random Forest classifier
    : returns: The model prediction - 'Ham' or 'Spam'
    """
    email = email.lower().replace('\n', '').translate(str.maketrans('', '', string.punctuation))
    email_vectorized = new_vectorizer_model.fit_transform([email])
    email_vectorized = pd.DataFrame(email_vectorized.toarray(), columns=new_vectorizer_model.get_feature_names())
    return 'Ham' if loaded_rfc_model_for_SOH.predict(email_vectorized)[0] == 0 else 'Spam'

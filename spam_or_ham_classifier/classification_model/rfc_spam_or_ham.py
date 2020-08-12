import pickle
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer


filename_vectorizer_model_for_SOH = 'vectorizer_model_for_SOH.pkl'
loaded_vectorizer_model_for_SOH = pickle.load(open(filename_vectorizer_model_for_SOH, 'rb'))

filename_rfc_model_for_SOH = 'rfc_model_for_SOH.pkl'
loaded_rfc_model_for_SOH = pickle.load(open(filename_rfc_model_for_SOH, 'rb'))

new_vectorizer_model = CountVectorizer(vocabulary=loaded_vectorizer_model_for_SOH.get_feature_names(),
                                       encoding='utf-8', decode_error='ignore',stop_words = 'english',
                                         analyzer='word', ngram_range=(1, 2),max_features=500)

def predict_SOH(email):
    email_vectorized = new_vectorizer_model.fit_transform([email])
    email_vectorized = pd.DataFrame(email_vectorized.toarray(), columns=new_vectorizer_model.get_feature_names())
    return loaded_rfc_model_for_SOH.predict(email_vectorized)[0]

from flask import Flask, request, jsonify
import pickle
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
print('ffff')

# Load the pickled model
with open('AmazonAlexaReviewsAnalysis.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

# Load the pickled CountVectorizer
with open('CountVectorizer.pkl', 'rb') as vectorizer_file:
    vectorizer = pickle.load(vectorizer_file)

# Load necessary preprocessing functions
def process_review(rev):
    """Process review function.
    Input:
        rev: a string containing a review
    Output:
        rev_clean: a list of words containing the processed review
    """
    stemmer = PorterStemmer()
    stopwords_english = set(stopwords.words('english'))
    # tokenize reviews
    tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True, reduce_len=True)
    rev_tokens = tokenizer.tokenize(rev)

    rev_clean = []
    for word in rev_tokens:
        if (word not in stopwords_english and  # remove stopwords
                word not in string.punctuation and word not in ["'"] and word.isalpha()):  # remove punctuation
            stem_word = stemmer.stem(word)  # stemming word
            rev_clean.append(stem_word)

    return rev_clean

@app.route('/predict', methods=['POST'])
def predict():
    print('hiii')
    data = request.get_json()
    review = data['review']
    
    # Preprocess the review
    processed_review = process_review(review)
    processed_review_str = " ".join(processed_review)
    
    # Vectorize the processed review
    review_vectorized = vectorizer.transform([processed_review_str])
    
    # Use the model to make predictions
    prediction = model.predict(review_vectorized)[0]
    
    return jsonify({'prediction': prediction})

if __name__ == '__main__':
    app.run(debug=True)

nlp1 = '''
import re
import nltk
import math
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.corpus import stopwords


nltk.download('wordnet')
nltk.download('punkt')
nltk.download('stopwords')

def tokenize_sentence(text):
    return sent_tokenize(text)

def tokenize_word(text):
    words = [word for word in word_tokenize(text) if not is_stop_word(word)]
    return words

def lemmatize(word):
    lemmatizer=WordNetLemmatizer()
    return lemmatizer.lemmatize(word)

def is_stop_word(word):
    stop_words=set(stopwords.words('english'))
    return word.lower() in stop_words


def calculate_tf(word,sentence):
    words=tokenize_word(sentence)
    return words.count(word)/len(words)

def calculate_idf(word,sentences):
    no=sum(1 for sentence in sentences if word in tokenize_word(sentence))
    return math.log(len(sentences)/(no+1))

def calculate_tf_idf(sentence,sentences):
    words=set(tokenize_word(sentence))
    tf_idf_scores=0
    for word in words:
        tf=calculate_tf(word,sentence)
        idf=calculate_idf(word,sentences)
        tf_idf_scores+=tf*idf
    return tf_idf_scores

def find_max_sentence(scores):
    max_score=float('-inf')
    max_sentence=None
    for sentence,score in scores.items():
        if(score>max_score):
            max_score=score
            max_sentence=sentence
    return max_sentence

def n_largest(scores,n):
    sentences=[]
    for i in range(n):
        max_sentence=find_max_sentence(scores)
        sentences.append(max_sentence)
        del scores[max_sentence]
    return sentences

def summarize_text(text,length):
    sentences=tokenize_sentence(text)
    sentence_scores={{sentence:calculate_tf_idf(sentence,sentences) for sentence in sentences}}
    selected_sentences=n_largest(sentence_scores,length)
    summary=' '.join(selected_sentences)
    return summary

text = "Natural language processing (NLP) is an interdisciplinary subfield of computer science and linguistics.It is primarily concerned with giving computers the ability to support and manipulate human language. It involves processing natural language datasets, such as text corpora or speech corpora, using either rule-based or probabilistic (i.e. statistical and, most recently, neural network-based) machine learning approaches. The goal is a computer capable of understanding the contents of documents, including the contextual nuances of the language within them. The technology can then accurately extract information and insights contained in the documents as well as categorize and organize the documents themselves.Natural language processing has its roots in the 1940s.[1] Already in 1940, Alan Turing published an article titled Computing Machinery and Intelligence which proposed what is now called the Turing test as a criterion of intelligence, though at the time that was not articulated as a problem separate from artificial intelligence"
summary = summarize_text(text,5)
print(summary)
'''

nlp2 = '''
import re
from nltk.corpus import stopwords 
import matplotlib.pyplot as plt
import random
from adjustText import adjust_text
import numpy as np



def generate_word_cloud(text):
  
    text = text.lower()
    words = re.findall(r'\b\w+\b', text)


    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]

    word_freq = {}
    for word in words:
        word_freq[word] = word_freq.get(word, 0) + 1

 
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)

 
    colors = [plt.cm.jet(i/float(len(sorted_words))) for i in range(len(sorted_words))]

 
    plt.figure(figsize=(10, 8))
    texts = []
    for i, (word, freq) in enumerate(sorted_words):
        size = max(int(np.log(freq ) * 20), 15)  
        x = random.uniform(0.1, 0.9)
        y = random.uniform(0.1, 0.9)
        text = plt.text(x, y, word, fontsize=size, color=colors[i], ha='center', va='center')
        texts.append(text)

    adjust_text(texts)

    plt.axis('off')
    plt.show()


text = """
Natural language processing NLP is an interdisciplinary subfield of computer science and linguistics.
It is primarily concerned with giving computers the ability to support and manipulate human language. 
It involves processing natural language datasets, such as text corpora or speech corpora, 
using either rule-based or probabilistic  statistical and, most recently, neural network-based 
machine learning approaches The goal is a computer capable of "understanding" the contents of documents
including the contextual nuances of the language within them The technology can then accurately extract 
information and insights contained in the documents as well as categorize and organize the documents themselves'
"""
generate_word_cloud(text)

'''

nlp3 = '''
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
import numpy as np
import math
import nltk

nltk.download('stopwords')

df = pd.read_csv("Musical_instruments_reviews.csv")
X = df['reviewText']
y = df['overall'].apply(lambda x: -1 if x <= 2 else (1 if x >= 4 else 0))

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

stop_words = set(stopwords.words('english'))
preprocess = lambda text: ' '.join([word.lower() for word in word_tokenize(text) if word.isalpha() and word.lower() not in stop_words])
X_train = X_train.apply(preprocess)
X_test = X_test.apply(preprocess)

def calculate_tf(term, document):
    words = document.split()
    return words.count(term) / (len(words)+1)

def calculate_idf(term, documents):
    document_containing_term = sum(1 for document in documents if term in document.split())
    return math.log(len(documents) / (document_containing_term + 1)) if document_containing_term > 0 else 0

all_documents = X_train.tolist() + X_test.tolist()
idf_values = {term: calculate_idf(term, all_documents) for term in set(' '.join(all_documents).split())}

vocabulary = sorted(list(idf_values.keys()))

X_train_tfidf_manual = []
for document in X_train:
    tfidf_vector = [calculate_tf(term, document) * idf_values[term] for term in vocabulary]
    X_train_tfidf_manual.append(tfidf_vector)

X_test_tfidf_manual = []
for document in X_test:
    tfidf_vector = [calculate_tf(term, document) * idf_values[term] for term in vocabulary]
    X_test_tfidf_manual.append(tfidf_vector)

X_train_tfidf_manual = np.array(X_train_tfidf_manual)
X_test_tfidf_manual = np.array(X_test_tfidf_manual)

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
model = LogisticRegression()
model.fit(X_train_tfidf_manual, y_train)
y_pred = model.predict(X_test_tfidf_manual)
print(classification_report(y_test, y_pred))

new_text = "Worst Product"
new_text_tfidf_manual = [calculate_tf(term, preprocess(new_text)) * idf_values[term] for term in vocabulary]
predicted_sentiment = model.predict([new_text_tfidf_manual])
print("Predicted Sentiment:", "Positive" if predicted_sentiment[0] == 1 else "Neutral" if predicted_sentiment[0] == 0 else "Negative")

new_text = "ok product"
new_text_tfidf_manual = [calculate_tf(term, preprocess(new_text)) * idf_values[term] for term in vocabulary]
predicted_sentiment = model.predict([new_text_tfidf_manual])
print("Predicted Sentiment:", "Positive" if predicted_sentiment[0] == 1 else "Neutral" if predicted_sentiment[0] == 0 else "Negative")

new_text = "amazing product and highly recommended"
new_text_tfidf_manual = [calculate_tf(term, preprocess(new_text)) * idf_values[term] for term in vocabulary]
predicted_sentiment = model.predict([new_text_tfidf_manual])
print("Predicted Sentiment:", "Positive" if predicted_sentiment[0] == 1 else "Neutral" if predicted_sentiment[0] == 0 else "Negative")
'''

nlp4 = '''
import numpy as np
import re
import pandas as pd
import requests
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression

# Load the data
data = pd.read_csv('Musical_instruments_reviews.csv')

# Preprocess the text data
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text

data['reviewText'] = data['reviewText'].apply(preprocess_text)

X = data['reviewText']
y = data['overall'].apply(lambda x: -1 if x <= 2 else (1 if x >= 4 else 0))

def calculate_ngrams(docs, n):
    ngram_list = []
    for doc in docs:
        words = doc.split()
        doc_ngrams = [tuple(words[i:i+n]) for i in range(len(words)-n+1)]
        ngram_list.append(doc_ngrams)
    return ngram_list

def count_terms_in_doc(doc, vocabulary):
    term_counts = [0] * len(vocabulary)
    for term in doc:
        if term in vocabulary:
            index = list(vocabulary).index(term)
            term_counts[index] += 1
    return term_counts

def ngrams_to_vector(ngrams, vocabulary):
    vector = []
    for doc in ngrams:
        doc_counts = count_terms_in_doc(doc, vocabulary)
        vector.append(doc_counts)
    return vector

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1, stratify=y)

xtrain_ngrams = calculate_ngrams(x_train, 2)
xtest_ngrams = calculate_ngrams(x_test, 2)
vocabulary = set(gram for doc in xtrain_ngrams for gram in doc)

xtrain_vector = ngrams_to_vector(xtrain_ngrams, vocabulary)
xtest_vector = ngrams_to_vector(xtest_ngrams, vocabulary)

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# Create and train the Logistic Regression model
model = LogisticRegression()
model.fit(xtrain_vector, y_train)

from sklearn.metrics import classification_report
y_pred = model.predict(xtest_vector)
print(classification_report(y_test, y_pred))

review = "sometimes it is good sometimes it is bad"
review_ngrams = calculate_ngrams([review], 2)
review_vector = ngrams_to_vector(review_ngrams, vocabulary)
res = model.predict(review_vector)
print(res[0])  # Prediction for the review

review = "amazing product and highly recommended"
review_ngrams = calculate_ngrams([review], 2)
review_vector = ngrams_to_vector(review_ngrams, vocabulary)
res = model.predict(review_vector)
print(res[0])  # Prediction for the 

review = "Product was very bad and crap and piece of shit"
review_ngrams = calculate_ngrams([review], 2)
review_vector = ngrams_to_vector(review_ngrams, vocabulary)
res = model.predict(review_vector)
print(res[0]-1)  # Prediction for the review
'''

nlp5 = '''
import numpy as np
import re
import pandas as pd
from collections import Counter
import requests
from sklearn.naive_bayes import MultinomialNB

# Load the data
data = pd.read_csv('Musical_instruments_reviews.csv')

# Preprocess the text data
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text

data['reviewText'] = data['reviewText'].apply(preprocess_text)

X = data['reviewText']
y = data['overall'].apply(lambda x: -1 if x <= 2 else (1 if x >= 4 else 0))

def calculate_ngrams(docs, n):
    ngram_list = []
    for doc in docs:
        words = doc.split()
        doc_ngrams = [tuple(words[i:i+n]) for i in range(len(words)-n+1)]
        ngram_list.append(doc_ngrams)
    return ngram_list

def count_terms_in_doc(doc, vocabulary):
    term_counts = [0] * len(vocabulary)
    for term in doc:
        if term in vocabulary:
            index = list(vocabulary).index(term)
            term_counts[index] += 1
    return term_counts

def ngrams_to_vector(ngrams, vocabulary):
    vector = []
    for doc in ngrams:
        doc_counts = count_terms_in_doc(doc, vocabulary)
        vector.append(doc_counts)
    return vector

from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

xtrain_ngrams = calculate_ngrams(X_train, 1)
xtest_ngrams = calculate_ngrams(X_test, 1)
vocabulary = set(gram for doc in xtrain_ngrams for gram in doc)

xtrain_vector = ngrams_to_vector(xtrain_ngrams, vocabulary)
xtest_vector = ngrams_to_vector(xtest_ngrams, vocabulary)

model = MultinomialNB()
model.fit(xtrain_vector, y_train)

from sklearn.metrics import classification_report
y_pred = model.predict(xtest_vector)
print(classification_report(y_test, y_pred))

review = "sometimes it is good sometimes it is bad"
review_ngrams = calculate_ngrams([review], 1)
review_vector = ngrams_to_vector(review_ngrams, vocabulary)
res = model.predict(review_vector)
print(res[0])  # Prediction for the 

review = "amazing product and highly recommended"
review_ngrams = calculate_ngrams([review], 1)
review_vector = ngrams_to_vector(review_ngrams, vocabulary)
res = model.predict(review_vector)
print(res[0])  # Prediction for the review

review = "Product was very bad and crap and piece of shit"
review_ngrams = calculate_ngrams([review], 1)
review_vector = ngrams_to_vector(review_ngrams, vocabulary)
res = model.predict(review_vector)
print(res[0])  # Prediction for the review
'''

nlp6 = '''
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
import numpy as np
import math
import nltk

nltk.download('stopwords')

df = pd.read_csv("spam.csv",encoding="Windows-1252")
X = df['v2']
y = df['v1'].apply(lambda x: 1 if x == "ham" else 0)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

stop_words = set(stopwords.words('english'))
preprocess = lambda text: ' '.join([word.lower() for word in word_tokenize(text) if word.isalpha() and word.lower() not in stop_words])
X_train = X_train.apply(preprocess)
X_test = X_test.apply(preprocess)

def calculate_tf(term, document):
    words = document.split()
    return words.count(term) / (len(words)+1)

def calculate_idf(term, documents):
    document_containing_term = sum(1 for document in documents if term in document.split())
    return math.log(len(documents) / (document_containing_term + 1)) if document_containing_term > 0 else 0

all_documents = X_train.tolist() + X_test.tolist()
idf_values = {term: calculate_idf(term, all_documents) for term in set(' '.join(all_documents).split())}

vocabulary = sorted(list(idf_values.keys()))

X_train_tfidf_manual = []
for document in X_train:
    tfidf_vector = [calculate_tf(term, document) * idf_values[term] for term in vocabulary]
    X_train_tfidf_manual.append(tfidf_vector)

X_test_tfidf_manual = []
for document in X_test:
    tfidf_vector = [calculate_tf(term, document) * idf_values[term] for term in vocabulary]
    X_test_tfidf_manual.append(tfidf_vector)

X_train_tfidf_manual = np.array(X_train_tfidf_manual)
X_test_tfidf_manual = np.array(X_test_tfidf_manual)

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
model = RandomForestClassifier()
model.fit(X_train_tfidf_manual, y_train)
y_pred = model.predict(X_test_tfidf_manual)
print(classification_report(y_test, y_pred))

new_text = "I HAVE A DATE ON SUNDAY WITH WILL!!"
new_text_tfidf_manual = [calculate_tf(term, preprocess(new_text)) * idf_values[term] for term in vocabulary]
predicted_sentiment = model.predict([new_text_tfidf_manual])
print("Predicted Sentiment:", "Not Spam" if predicted_sentiment[0] == 1 else "Spam")

new_text = "URGENT! You have won a 1 week FREE membership in our �100,000 Prize Jackpot!"
new_text_tfidf_manual = [calculate_tf(term, preprocess(new_text)) * idf_values[term] for term in vocabulary]
predicted_sentiment = model.predict([new_text_tfidf_manual])
print("Predicted Sentiment:", "Not Spam" if predicted_sentiment[0] == 1 else "Spam")
'''

nlp7 = '''
import pandas as pd
import matplotlib.pyplot as plt

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

import gensim
from gensim.corpora import Dictionary
from gensim.models import LsiModel

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

df = pd.read_csv("quora_questions.csv")
data = df.sample(n=1000, axis=0)
data = data['Question']

stop_words = set(stopwords.words("english"))


def preprocess(text):
    text = text.lower()
    words = word_tokenize(text)
    words = [word for word in words if word not in stop_words]
    import re
    special_chars = r'[,.:;?\(\'"\s]'
    words = [re.sub(special_chars, '', word) for word in words]
    return words


data = data.apply(preprocess)
dictionary = Dictionary(data)
dictionary.filter_extremes(no_below=5, no_above=0.5)
bow_corpus = [dictionary.doc2bow(text) for text in data]

num_topics = 5
lsamodel = LsiModel(bow_corpus, num_topics=num_topics, id2word=dictionary)

topics = lsamodel.show_topics(num_topics=num_topics, num_words=10)
top_topics = []
for topic in topics:
    top_topics.append(topic[1])

print("Top 5 LSA Topics:")
for i, topic in enumerate(top_topics, start=1):
    print(f"Topic {{i}} : {{topic}}")
'''

def Nlp1():
    return nlp1

def Nlp2():
    return nlp2

def Nlp3():
    return nlp3

def Nlp4():
    return nlp4

def Nlp5():
    return nlp5

def Nlp6():
    return nlp6

def Nlp7():
    return nlp7
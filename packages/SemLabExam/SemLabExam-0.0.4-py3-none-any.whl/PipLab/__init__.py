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
    sentence_scores={sentence:calculate_tf_idf(sentence,sentences) for sentence in sentences}
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
    words = re.findall(r'\\b\w+\\b', text)


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
    special_chars = r'[,.:;?\(\\'"\s]'
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
    print(f"Topic {i} : {topic}")
'''

aiml1 = '''
def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("---------")

def check_winner(board, player):
    for i in range(3):
        if all(board[i][j] == player for j in range(3)) or all(board[j][i] == player for j in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

def is_board_full(board):
    return all(board[i][j] != ' ' for i in range(3) for j in range(3))

def dfs(board, player):
    if check_winner(board, 'X'):
        return 1
    elif check_winner(board, 'O'):
        return -1
    elif is_board_full(board):
        return 0

    scores = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = player
                if player == 'X':
                    scores.append(dfs(board, 'O'))
                else:
                    scores.append(dfs(board, 'X'))
                board[i][j] = ' '

    if player == 'X':
        return max(scores)
    else:
        return min(scores)

def find_best_move(board):
    best_score = float('-inf')
    best_move = (-1, -1)
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = 'X'
                score = dfs(board, 'O')
                board[i][j] = ' '
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    return best_move

def play_game():
    board = [[' ' for _ in range(3)] for _ in range(3)]
    current_player = 'X'
    while True:
        print_board(board)
        if current_player == 'X':
            row, col = find_best_move(board)
            board[row][col] = 'X'
        else:
            while True:
                row = int(input("Enter row (0-2): "))
                col = int(input("Enter column (0-2): "))
                if 0 <= row <= 2 and 0 <= col <= 2 and board[row][col] == ' ':
                    break
                else:
                    print("Invalid move. Try again.")
            board[row][col] = 'O'

        if check_winner(board, current_player):
            print_board(board)
            print(f"Player {current_player} wins!")
            break
        elif is_board_full(board):
            print_board(board)
            print("It's a tie!")
            break
        current_player = 'X' if current_player == 'O' else 'O'

play_game()
'''

aiml2 = '''
mini , maxi = -1000, 1000
def minimax(depth, nodeIndex, maxplay, values, alpha, beta):
    if depth == 3:
        return values[nodeIndex]
    
    if maxplay:
        best = mini
        for i in range(0,2):
            val = minimax(depth+1,nodeIndex*2+i,False,values,alpha,beta)
            best = max(best,val)
            alpha = max(alpha,best)
            if beta <= alpha:
                break
        return best
    
    else:
        best = maxi
        for i in range(0,2):
            val = minimax(depth+1,nodeIndex*2+i,True,values,alpha,beta)
            best = min(best,val)
            beta = min(beta,best)
            if beta <= alpha:
                break
        return best


if __name__ == "__main__":
    values = [3,2,8,4,1,9,6,5]
    print(minimax(0,0,True,values,mini,maxi))

COUNT = [10]

class newNode:

    def __init__(self, key):
        self.data = key
        self.left = None
        self.right = None

def print2DUtil(root, space):
    if (root == None):
        return

    space += COUNT[0]
    print2DUtil(root.right, space)
    print()
    for i in range(COUNT[0], space):
        print(end=" ")
    print(root.data)
    print2DUtil(root.left, space)


def print2D(root):
    print2DUtil(root, 0)


# Driver Code
if __name__ == '__main__':

    root = newNode("A")
    root.left = newNode("B")
    root.right = newNode("c")

    root.left.left = newNode("D")
    root.left.right = newNode("E")
    root.right.left = newNode("F")
    root.right.right = newNode("G")

    root.left.left.left = newNode(3)
    root.left.left.right = newNode(2)
    root.left.right.left = newNode(8)
    root.left.right.right = newNode(4)
    root.right.left.left = newNode(1)
    root.right.left.right = newNode(9)
    root.right.right.left = newNode(6)
    root.right.right.right = newNode(5)

    print2D(root)
'''

aiml3 = '''
class Node:
    
    def __init__(self,state,parent,g,h):
        self.state = state
        self.parent = parent
        self.g = g
        self.h = h
        self.f = g + h
        
    def __lt__(self, other):
        return self.f < other.f
    
    def neighbors(self):
        neighbors = []
        zero_index = self.state.index(0)
        row, col = divmod(zero_index, 3)

        if col > 0:
            new_state = self.state[:]
            new_state[zero_index], new_state[zero_index - 1] = new_state[zero_index - 1], new_state[zero_index]
            neighbors.append(new_state)

        if col < 2:
            new_state = self.state[:]
            new_state[zero_index], new_state[zero_index + 1] = new_state[zero_index + 1], new_state[zero_index]
            neighbors.append(new_state)

        if row > 0:
            new_state = self.state[:]
            new_state[zero_index], new_state[zero_index - 3] = new_state[zero_index - 3], new_state[zero_index]
            neighbors.append(new_state)

        if row < 2:
            new_state = self.state[:]
            new_state[zero_index], new_state[zero_index + 3] = new_state[zero_index + 3], new_state[zero_index]
            neighbors.append(new_state)

        return neighbors
    
    def path(self):
        path = []
        current_node = self
        while current_node:
            path.append(current_node.state)
            current_node = current_node.parent
        path.reverse()
        return path

def manhattan_distance(state1, state2):
    distance = 0
    for i in range(len(state1)):
        if state1[i] != state2[i]:
            distance += 1
    return distance

import heapq
def a_star(start, goal):
    open_list = []
    closed_list = []

    heapq.heappush(open_list, Node(start, None, 0, manhattan_distance(start, goal)))

    while open_list:
        current = heapq.heappop(open_list)

        if current.state == goal:
            return current.path()

        closed_list.append(current)

        for neighbor_state in current.neighbors():
            neighbor = Node(neighbor_state, current, current.g + 1, manhattan_distance(neighbor_state, goal))
            if neighbor not in closed_list:
                heapq.heappush(open_list, neighbor)

def print_path(path):
    count = 0
    for step, state in enumerate(path):
        print(f"\\nStep {step + 1}:\\n")
        for row in state:
            print(row,end=" ")
            count = count + 1
            if count%3 == 0:
                print("\\n")

if __name__ == '__main__':
    start = []
    goal = []
    print("Enter the start puzzle :")
    for i in range(0,9):
        node = int(input())
        start.append(node)
        
    print("Enter the goal puzzle :")
    for i in range(0,9):
        node = int(input())
        goal.append(node)
    
    path = a_star(start, goal)

    if path:
        print_path(path)
    else:
        print('No solution found.')
            
'''

aiml4 = '''
arr = []

def poly():
    while True:
        power = int(input("Enter the power : "))
        coeff = int(input("Enter the coeffecient : "))
        term = []
        term.append(power)
        term.append(coeff)
        arr.append(term)
        if power == 0:
            break
            
def func(x):
    fun = 0
    for term in arr:
        fun = fun + (term[1]*pow(x,term[0]))
        
    return fun

import math
def trig_func(x):
    return math.sin(x)

def combined_func(x):
    return func(x) + trig_func(x)

def hill_climbing_search(x0, delta, tol=1e-6, max_iter=10000):
    x = x0
    i = 0

    while True:
        i += 1

        x_up = x + delta
        x_down = x - delta

        f_x_up = combined_func(x_up)
        f_x_down = combined_func(x_down)

        if i > max_iter:
            print("Max iterations reached.")
            break

        if f_x_up < f_x_down:
            x = x_down
        else:
            x = x_up

        if abs(x - x0) < tol:
            break

        x0 = x

    return x

import random
x0 = float(input("Enter the values of x0 : "))
maxis = []
deltas = []
for i in range(0,10):
    delta = random.random()
    deltas.append(delta)
    x_max = hill_climbing_search(x0,delta)
    maxis.append(x_max)
    print(f"The value of x that maximises the function is {x_max}.")

import matplotlib.pyplot as plt
plt.plot(maxis)
'''

aiml5 = '''
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import pandas as pd

class LogisticRegression:
    def __init__(self, learning_rate=0.001, iterations=2000):
        self.learning_rate = learning_rate
        self.iterations = iterations

    def add_intercept(self, X):
        intercept = np.ones((X.shape[0], 1))
        return np.concatenate((intercept, X), axis=1)

    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))

    def cost(self, h, y):
        return (-y * np.log(h) - (1 - y) * np.log(1 - h)).mean()

    def fit(self, X, y):
        X = self.add_intercept(X)
        self.theta = np.zeros(X.shape[1])

        for _ in range(self.iterations):
            z = np.dot(X, self.theta)
            h = self.sigmoid(z)
            gradient = np.dot(X.T, (h - y)) / y.size
            self.theta -= self.learning_rate * gradient

    def predict_prob(self, X):
        X = self.add_intercept(X)
        return self.sigmoid(np.dot(X, self.theta))

    def predict(self, X, threshold=0.5):
        return self.predict_prob(X) >= threshold

data = pd.read_csv("Breastcancer_data.csv")
X = data.iloc[:,2:32].values
X = np.float64(X)
y = data.iloc[:,1].values
y = np.where(y == 'M', 1, 0)
y.shape

X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=0)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=0)

model = LogisticRegression()
model.fit(X_train, y_train)
val_predictions = model.predict(X_val)
val_predictions_prob = model.predict_prob(X_val)
print(val_predictions_prob)

accuracy = accuracy_score(y_val, val_predictions)
precision = precision_score(y_val, val_predictions)
recall = recall_score(y_val, val_predictions)
f1 = f1_score(y_val, val_predictions)

print("Validation Set Metrics:")
print("Accuracy: {:.2f}".format(accuracy))
print("Precision: {:.2f}".format(precision))
print("Recall: {:.2f}".format(recall))
print("F1 Score: {:.2f}".format(f1))

from sklearn.metrics import confusion_matrix
confusion = confusion_matrix(y_val,val_predictions)
print(confusion)
print("Class 0 predicted and true : ")
print(confusion[0][0])
print("Class 0 predicted and false : ")
print(confusion[0][1])
print("Class 1 predicted and false : ")
print(confusion[1][0])
print("Class 1 predicted and true : ")
print(confusion[1][1])

import random
X_valid = []
Y_valid = []
for i in range (0,20):
    index = random.randint(0,500)
    X_valid.append(X[index])
    Y_valid.append(y[index])
    
Y_valid

data = pd.read_csv("Valid_Data.csv")
X = np.float64(X_valid)

val_predictions = model.predict(X)
val_predictions

accuracy = accuracy_score(Y_valid, val_predictions)
precision = precision_score(Y_valid, val_predictions)
recall = recall_score(Y_valid, val_predictions)
f1 = f1_score(Y_valid, val_predictions)

print("Validation Set Metrics:")
print("Accuracy: {:.2f}".format(accuracy))
print("Precision: {:.2f}".format(precision))
print("Recall: {:.2f}".format(recall))
print("F1 Score: {:.2f}".format(f1))

from sklearn.metrics import confusion_matrix
confusion = confusion_matrix(Y_valid,val_predictions)
print(confusion)
print("Class 0 predicted and true : ")
print(confusion[0][0])
print("Class 0 predicted and false : ")
print(confusion[0][1])
print("Class 1 predicted and false : ")
print(confusion[1][0])
print("Class 1 predicted and true : ")
print(confusion[1][1])

import matplotlib.pyplot as plt
acc = []
iterations = 0
for i in range (0,10):
    learning_rate = random.randint(1,9)
    learning_rate = learning_rate/1000
    iterations = 100 + iterations
    model = LogisticRegression(learning_rate=learning_rate,iterations=iterations)
    model.fit(X_train, y_train)
    val_predictions = model.predict(X)
    accuracy = accuracy_score(Y_valid, val_predictions)
    acc.append(accuracy)

print(acc)

x = [100,200,300,400,500,600,700,800,900,1000]
plt.xlabel("No. of iterations")
plt.ylabel("Accuracy")
plt.plot(x,acc)
'''

aiml6 = '''
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,precision_score,f1_score,recall_score
def read_data(file_path):
    return pd.read_csv(file_path)

class NaiveBayes():
    def __init__(self):
        self.class_prob={}
        self.features_prob={}
    def fit(self,X_train,Y_train):
        classes,counts=np.unique(Y_train,return_counts=True)
        total_samples=len(Y_train)
        for c,count in zip(classes,counts):
            self.class_prob[c]=count/total_samples
        self.features_prob={}
        for c in classes:
            self.features_prob[c]={}
            for feature in X_train.columns:
                unique_values=X_train[feature].unique()
                self.features_prob[c][feature]={}
                for value in unique_values:
                    count = np.sum((X_train[feature] == value) & (Y_train == c))
                    self.features_prob[c][feature][value] = count / counts[c]
                   
                   
    def predict(self,X_test):
        predictions=[]
        for _,row in X_test.iterrows():
            max_prob=-1
            predicted_class=None
            for c in self.class_prob:
                prob = self.class_prob[c]
                for feature, value in row.items():
                    if value in self.features_prob[c][feature]:
                        prob *= self.features_prob[c][feature][value]
                    else:
                        prob *= 0
                if prob > max_prob:
                    max_prob = prob
                    predicted_class = c
                predictions.append(predicted_class)
        return predictions

data = read_data("Social_Network_Ads.csv")
data['Gender'] = data['Gender'].apply(lambda x: 1 if x == "Male" else 0)
X = data.iloc[:,1:4]
y = data['Purchased']
X_train,X_test,Y_train,Y_test=train_test_split(X,y,test_size=0.2,random_state=0)

model=NaiveBayes()
model.fit(X_train,Y_train)
Y_pred=model.predict(X_test)

y_pred = []
for i in range(len(Y_pred)):
    if i % 2 != 0:
        y_pred.append(Y_pred[i])
Y_test = Y_test.tolist()

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

accuracy = accuracy_score(y_pred, Y_test)
precision = precision_score(y_pred, Y_test)
recall = recall_score(y_pred, Y_test)
f1 = f1_score(y_pred, Y_test)

print("Validation Set Metrics:")
print("Accuracy: {:.2f}".format(accuracy))
print("Precision: {:.2f}".format(precision))
print("Recall: {:.2f}".format(recall))
print("F1 Score: {:.2f}".format(f1))

confusion = confusion_matrix(y_pred,Y_test)
print(confusion)
print("Class 0 predicted and true : ")
print(confusion[0][0])
print("Class 0 predicted and false : ")
print(confusion[0][1])
print("Class 1 predicted and false : ")
print(confusion[1][0])
print("Class 1 predicted and true : ")
print(confusion[1][1])

valid = data.sample(n=20)
X_valid = valid.iloc[:,1:4]
y_valid = valid['Purchased']

y_val = model.predict(X_valid)
y_valpred = []
for i in range(len(y_val)):
    if i % 2 != 0:
        y_valpred.append(y_val[i])
y_valid = y_valid.tolist()

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

accuracy = accuracy_score(y_valpred,y_valid)
precision = precision_score(y_valpred,y_valid)
recall = recall_score(y_valpred,y_valid)
f1 = f1_score(y_valpred,y_valid)

print("Validation Set Metrics:")
print("Accuracy: {:.2f}".format(accuracy))
print("Precision: {:.2f}".format(precision))
print("Recall: {:.2f}".format(recall))
print("F1 Score: {:.2f}".format(f1))

confusion = confusion_matrix(y_valpred,y_valid)
print(confusion)
print("Class 0 predicted and true : ")
print(confusion[0][0])
print("Class 0 predicted and false : ")
print(confusion[0][1])
print("Class 1 predicted and false : ")
print(confusion[1][0])
print("Class 1 predicted and true : ")
print(confusion[1][1])
'''

aiml7 = '''
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

df = pd.read_csv('iris_csv.csv')

X = df.iloc[:, :4]  
y = df.iloc[:, -1]   
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

def euclidean_distance(point1, point2):
    return np.sqrt(np.sum((point1 - point2) ** 2))

def knn_predict(train_data, train_labels, test_point, k=3):
    distances = []

    for i in range(len(train_data)):
        distance = euclidean_distance(test_point, train_data.iloc[i, :])
        distances.append((distance, train_labels.iloc[i]))

    sorted_distances = sorted(distances, key=lambda x: x[0])
    k_nearest_neighbors = sorted_distances[:k]
    class_counts = {}
    for neighbor in k_nearest_neighbors:
        label = neighbor[1]
        class_counts[label] = class_counts.get(label, 0) + 1
    predicted_class = max(class_counts, key=class_counts.get)
    return predicted_class

pred = [knn_predict(X_train, y_train, X_test.iloc[i, :], k=3) for i in range(len(X_test))]

from sklearn.metrics import accuracy_score,precision_score,f1_score,recall_score,confusion_matrix
accuracy = accuracy_score(y_test, pred)
precision = precision_score(y_test, pred,average='micro')
recall = recall_score(y_test, pred,average='micro')
f1 = f1_score(y_test, pred,average='micro')

print("Validation Set Metrics:")
print("Accuracy: {:.2f}".format(accuracy))
print("Precision: {:.2f}".format(precision))
print("Recall: {:.2f}".format(recall))
print("F1 Score: {:.2f}".format(f1))

confusion = confusion_matrix(y_test, pred)
print("Class 0 predicted and true : ")
print(confusion[0][0])
print("Class 0 predicted and false : ")
print(confusion[0][1])
print("Class 1 predicted and false : ")
print(confusion[1][0])
print("Class 1 predicted and true : ")
print(confusion[1][1])

valid = df.sample(n=20)
X_valid = valid.iloc[:, :4]
y_valid = valid.iloc[:, -1]

val_pred = [knn_predict(X_train, y_train, X_valid.iloc[i, :], k=3) for i in range(len(X_valid))]

accuracy = accuracy_score(y_valid, val_pred)
precision = precision_score(y_valid, val_pred,average='micro')
recall = recall_score(y_valid, val_pred,average='micro')
f1 = f1_score(y_valid, val_pred,average='micro')

print("Validation Set Metrics:")
print("Accuracy: {:.2f}".format(accuracy))
print("Precision: {:.2f}".format(precision))
print("Recall: {:.2f}".format(recall))
print("F1 Score: {:.2f}".format(f1))

confusion = confusion_matrix(y_valid,val_pred)
print("Class 0 predicted and true : ")
print(confusion[0][0])
print("Class 0 predicted and false : ")
print(confusion[0][1])
print("Class 1 predicted and false : ")
print(confusion[1][0])
print("Class 1 predicted and true : ")
print(confusion[1][1])
'''

aiml8 = '''
import numpy as np
from sklearn.datasets import load_iris
import matplotlib.pyplot as plt

class KMeans:
    def __init__(self, n_clusters, max_iters=100):
        self.n_clusters = n_clusters
        self.max_iters = max_iters

    def fit(self, X):
        # Initialize centroids randomly
        self.centroids = X[np.random.choice(X.shape[0], self.n_clusters, replace=False)]
        
        for _ in range(self.max_iters):
            # Assign each data point to the nearest centroid
            labels = self._assign_labels(X)
            
            # Update centroids
            new_centroids = self._update_centroids(X, labels)
            
            # Check for convergence
            if np.all(self.centroids == new_centroids):
                break
                
            self.centroids = new_centroids

    def _assign_labels(self, X):
        # Compute distances from each data point to centroids
        distances = np.linalg.norm(X[:, np.newaxis] - self.centroids, axis=2)
        
        # Assign labels based on the nearest centroid
        return np.argmin(distances, axis=1)
    
    def _update_centroids(self, X, labels):
        new_centroids = np.array([X[labels == i].mean(axis=0) for i in range(self.n_clusters)])
        return new_centroids

iris = load_iris()
X = iris.data[:, :2]
kmeans = KMeans(n_clusters=4)

kmeans.fit(X)
labels = kmeans._assign_labels(X)

print("Cluster Assignments:", labels)
print("Final Centroids:", kmeans.centroids)

plt.scatter(X[:, 0], X[:, 1], c=labels)
plt.scatter(kmeans.centroids[:, 0], kmeans.centroids[:, 1], c='red', marker='x',label='Centroids')
plt.title('K-Means Clustering')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')

plt.show()
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

def Aiml1():
    return aiml1

def Aiml2():
    return aiml2

def Aiml3():
    return aiml3

def Aiml4():
    return aiml4

def Aiml5():
    return aiml5

def Aiml6():
    return aiml6

def Aiml7():
    return aiml7

def Aiml8():
    return aiml8
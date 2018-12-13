import gensim
import pandas as pd
import os
import re
import nltk
from nltk.corpus import wordnet as wn
from sklearn.feature_extraction.text import TfidfVectorizer

import settings
from loader import Loader

class Sentiment():
    def __init__(self):
        # Load dataset
        l = Loader()
        self.positive_words, self.negative_words, self.neutral_words = l.load_word_sentiments()

        self.data = l.load_dataset()

        # Stopwords
        self.en_stop, self.fil_stop = l.load_stop_words()

        # Word2vec
        self.tokenized_data = []
        self.model = None
        self.model_sparse = None

    def get_lemma(self, word):
        lemma = wn.morphy(word)
        if lemma is None:
            return word
        else:
            return lemma
    
    def tokenize_data(self):
        print('[debug] tokenize')
        self.tokenized_data = []
        counter = 0
        index = 0

        for line in self.data:
            tokens = gensim.utils.simple_preprocess(line)
            tokens = [re.sub('\#ADMUFreedomWall\ \d+', '', sent) for sent in tokens]
            tokens = [re.sub('\#ADMUFreedomWall\d+', '', sent) for sent in tokens]
            tokens = [word for word in tokens if word not in self.fil_stop]
            tokens = [word for word in tokens if word not in self.en_stop]
            tokens = [word for word in tokens if len(word) > 2]
            tokens = [self.get_lemma(token) for token in tokens]
            
            self.tokenized_data.append(tokens)
            counter += len(tokens)
            index+=1
            
        print('Words in tokenized data: ', counter)
        numbers_set = set(i for j in self.tokenized_data for i in j)
        print('Unique tokens:', len(numbers_set))

    def create_word2vec(self):
        self.model = gensim.models.Word2Vec(self.tokenized_data, size=50, window=5, min_count=5, workers=4)
        self.model.train(self.tokenized_data, total_examples=len(self.tokenized_data) , epochs=100)
        # For words that dont occur as much
        self.model_sparse = gensim.models.Word2Vec(self.tokenized_data, size=50, window=5, min_count=1, workers=4)
        self.model_sparse.train(self.tokenized_data, total_examples=len(self.tokenized_data) , epochs=100)

    def get_sentiment(self, sentence):
        tokens = sentence.split(' ')
        sum_score = 0
        relevant_words = 0
        
        for token in tokens:
            if token in self.positive_words:
                print("Word: " + token + ", score: 1")
                print()
                sum_score += 1
                relevant_words += 1
            elif token in self.negative_words:
                print("Word: " + token + ", score: -1")
                print()
                sum_score -= 1
                relevant_words += 1
            elif token in self.neutral_words:
                print("Word: " + token)
                try:
                    neighbors = self.model.wv.most_similar(positive=token, topn=100)
                except:
                    try:
                        neighbors = self.model_sparse.wv.most_similar(positive=token,topn=100)
                    except:
                        pass
                for word in neighbors:
                    if word[0] in self.positive_words:
                        print("Nearest labelled word: " + word[0] + ", score: " + str(word[1]))
                        print()
                        sum_score += word[1]
                        relevant_words += 1
                        break
                    elif word[0] in self.negative_words:
                        print("Nearest labelled word: " + word[0] + ", score: -" + str(word[1]))
                        print()
                        sum_score -= word[1]
                        relevant_words += 1
                        break
            else:
                pass
    #             print('"' + token + '" not in model')
        val = sum_score/relevant_words
        return val

    



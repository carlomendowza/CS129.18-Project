import gensim
import pandas as pd
import numpy as np
import os
import re
import nltk
from nltk.corpus import wordnet as wn
from sklearn.feature_extraction.text import TfidfVectorizer
from pprint import pprint

import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel

import spacy

import settings
from loader import Loader
from senti import Sentiment

class Topic_Modeling():
    def __init__(self):
        # Load dataset
        l  = Loader()
        self.data = l.load_dataset_topic_ver()

        self.data_words = None

        # Load sentiment analysis
        self.s = None
        
        # Stopwords
        self.en_stop, self.fil_stop = l.load_stop_words()

        # Bigrams and Trigrams
        self.bigram = None
        self.bigram_mod = None
        self.trigram = None
        self.trigram_mod = None

        # Lemmatized
        self.data_lemmatized = None

        # Corpus
        self.id2word = None
        self.texts = None
        self.corpus = None

        # LDA
        self.optimal_model = None

    def tokenize(self):
        def sent_to_words(sentences):
            for sentence in sentences:
                yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))  # deacc=True removes punctuations
        self.data_words = list(sent_to_words(self.data))
        

    def create_bigrams(self, data, min_count=5, threshold=100):
        print('[debug] creating bigrams')
        self.bigram = gensim.models.Phrases(data, min_count=min_count, threshold=threshold) # higher threshold fewer phrases.
        self.bigram_mod = gensim.models.phrases.Phraser(self.bigram)

    def create_trigrams(self, data, threshold=100):
        print('[debug] creating trigrams')
        self.trigram = gensim.models.Phrases(self.bigram[self.data_words], threshold=threshold)  
        self.trigram_mod = gensim.models.phrases.Phraser(self.trigram)

    """ Functions used by lemmatize_data """
    def remove_stopwords(self, texts):
        output = [[word for word in simple_preprocess(str(doc)) if (word not in self.en_stop and word not in self.fil_stop)] for doc in texts]
        return output

    def make_bigrams(self, texts):
        return [self.bigram_mod[doc] for doc in texts]

    def make_trigrams(self, texts):
        return [self.trigram_mod[self.bigram_mod[doc]] for doc in texts]

    def lemmatization(self, texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
        nlp = spacy.load('en', disable=['parser', 'ner'])
        texts_out = []
        for sent in texts:
            doc = nlp(" ".join(sent)) 
            texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
        return texts_out

    """ end """

    def lemmatize_data(self):
        print('[debug] lemmatize')
        data_words_nostops = self.remove_stopwords(self.data_words)
        data_words_bigrams = self.make_bigrams(data_words_nostops)
        nlp = spacy.load('en', disable=['parser', 'ner'])
        self.data_lemmatized = self.lemmatization(data_words_bigrams, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])

    def create_corpus(self):
        print('[debug] creating corpus')
        self.id2word = corpora.Dictionary(self.data_lemmatized)
        self.texts = self.data_lemmatized
        self.corpus = [self.id2word.doc2bow(text) for text in self.texts]

    def build_LDA(self, num_topics=20, random_state=100, update_every=1, chunksize=100, passes=10, alpha='auto', per_word_topics=True):
        print('[debug] building LDA model')
        num_topics = num_topics
        lda_model = gensim.models.ldamodel.LdaModel(corpus=self.corpus,
                                                id2word=self.id2word,
                                                num_topics=num_topics, 
                                                random_state=random_state,
                                                update_every=update_every,
                                                chunksize=chunksize,
                                                passes=passes,
                                                alpha=alpha,
                                                per_word_topics=per_word_topics)
        doc_lda = lda_model[self.corpus]
        mallet_path = settings.MALLET_PATH
        ldamallet = gensim.models.wrappers.LdaMallet(mallet_path, corpus=self.corpus, num_topics=num_topics, id2word=self.id2word)
        coherence_model_ldamallet = CoherenceModel(model=ldamallet, texts=self.data_lemmatized, dictionary=self.id2word, coherence='c_v')
        coherence_ldamallet = coherence_model_ldamallet.get_coherence()
        print('Coherence Score: ', coherence_ldamallet)
        self.optimal_model = ldamallet

    def compute_coherence_values(dictionary, corpus, texts, limit, start=2, step=3):
        coherence_values = []
        model_list = []
        for num_topics in range(start, limit, step):
            model = gensim.models.wrappers.LdaMallet(mallet_path, corpus=corpus, num_topics=num_topics, id2word=id2word)
            model_list.append(model)
            coherencemodel = CoherenceModel(model=model, texts=texts, dictionary=dictionary, coherence='c_v')
            coherence_values.append(coherencemodel.get_coherence())

        return model_list, coherence_values

    def show_model_topics(self, num_words=10):
        model_topics = self.optimal_model.show_topics(formatted=False)
        pprint(self.optimal_model.print_topics(num_words=num_words))

    def get_topic(self,sentence):
        bow = self.id2word.doc2bow(simple_preprocess(sentence))
        topic_weights = self.optimal_model[bow]
        topic = [t[1] for t in topic_weights]
        topic_id = np.argmax(topic)
        return (topic_id)

    def get_sentence(self,sentence):
        test_string = sentence
        try:
            sent = self.s.get_sentiment(test_string)
            topic = self.get_topic(test_string)
            print(f'Sentiment: {sent}')
            print(f'Topic: {topic}')
        except Exception as e:
            print('Error:', e)


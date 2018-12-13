# Loads data and sentiments
import settings, os, re
import pandas as pd
import nltk


class Loader:
    # Returns the labelled words' sentiments
    def load_word_sentiments(self):
        positive_words, negative_words, neutral_words = [], [], []
        for directories, subdirs, files in os.walk(settings.ROOT_DIR):
            if (os.path.split(directories)[1] == '1' or os.path.split(directories)[1] == '2' or os.path.split(directories)[1] == '3' or os.path.split(directories)[1] == '4'):
                for filename in files:
                    if (filename == 'positive.txt'):
                        with open(os.path.join(directories, filename)) as f:
                            for line in f:
                                positive_words.append(line.strip())
                    if (filename == 'negative.txt'):
                        with open(os.path.join(directories, filename)) as f:
                            for line in f:
                                negative_words.append(line.strip())
                    if (filename == 'neutral.txt'):
                        with open(os.path.join(directories, filename), encoding='latin-1') as f:
                            for line in f:
                                neutral_words.append(line.strip())
        return positive_words, negative_words, neutral_words

    # Returns the post bodies in a list
    def load_dataset(self):
        df = pd.read_csv(settings.RAW_DATA_PATH)
        data = df['Body']
        data.dropna(inplace=True)
        data.drop_duplicates(inplace=True)
        return data

    # Returns the post bodies in a list, with some extra cleaning
    def load_dataset_topic_ver(self):
        text_data = []
        df = pd.read_csv(settings.RAW_DATA_PATH)
        data = df['Body']
        data.dropna(inplace=True)

        data = df['Body'].values.tolist()
        data = [re.sub('\S*@\S*\s?', '', sent) for sent in data]
        data = [re.sub('\s+', ' ', sent) for sent in data]
        data = [re.sub("\'", "", sent) for sent in data]
        data = [re.sub('\#ADMUFreedomWall\ \d+', '', sent) for sent in data]
        data = [re.sub('\#ADMUFreedomWall\d+', '', sent) for sent in data]

        return data
    
    
    def load_stop_words(self):
        print('[debug] stopwords')
        # English stop words
        nltk.download('stopwords')
        en_stop = nltk.corpus.stopwords.words('english')
        en_stop.extend(['from', 'subject', 're', 'edu', 'use'])

        # Filipino stop words
        fil_stop = []
        with open(settings.STOP_WORDS_PATH) as f:
            for line in f:
                fil_stop.append(line.rstrip('\n')) 
        nltk.download('wordnet')

        return en_stop, fil_stop

l = Loader()
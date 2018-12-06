import spacy
#spacy.load('en')
from nltk.tokenize import wordpunct_tokenize
from spacy.lang.en import English
parser = English()
import nltk
nltk.download('wordnet')
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
nltk.download('stopwords')
stopwords = nltk.corpus.stopwords.words('english')
from gensim import corpora
from itertools import groupby, product, chain
import pickle
import string
import gensim
import re
from nltk import word_tokenize
NUM_TOPICS = 20

class ModelGenerator(object):

    def __init__(self, threads):
        self.stopwords = nltk.corpus.stopwords.words('english')
        self.punctuations = string.punctuation
        self.ignore = set(chain(self.stopwords, self.punctuations))
        self.model = None
        self.dictionary = None
        self.topics = None
        self.data = None
        self.generate_data(threads)
        #print(self.data)
        self.generate_topics_dictionary()

    def get_topics(self):
        return self.topics


    def concat_thread(self, thread):
        string = ''
        for line in thread:
            string += line
        return string


    def generate_data(self, threads):

        self.data = []
        for thread in threads:
            line = self.concat_thread(thread)
            tokens = self.clean_text(line)
            self.data.append(tokens)


    def parse(self, text):
        phrases = set()

        for sentence in text:
            words = [word.lower() for word in wordpunct_tokenize(sentence)]
            phrases.update(self.generate_phrase_from_words(words))
        return phrases

    def generate_phrase_from_words(self, words):
        groups = groupby(words, lambda x : x not in self.ignore)
        phrases = [tuple(group[1]) for group in groups if group[0]]

        return phrases

    def clean_text(self, text):
        tokenized_text = word_tokenize(text.lower())
        cleaned_text = [t for t in tokenized_text if t not in self.ignore and re.match('[a-zA-Z\-][a-zA-Z\-]{2,}', t)]
        return cleaned_text

    def get_lemma(self, word):
        lemma = wn.morphy(word)
        if lemma is None:
            return word
        else:
            return lemma

    def process_text(self, text):
        tokens = self.parse(text)
        clean_tokens = []

        for t in tokens:
            if len(t) > 4 and t not in self.ignore:
                clean_tokens.append(self.get_lemma(t))

        return clean_tokens

    def generate_topics_dictionary(self):

        self.dictionary = corpora.Dictionary(self.data)
        corpus = [self.dictionary.doc2bow(text) for text in self.data]
        pickle.dump(corpus, open('corpus.pkl', 'wb'))
        self.dictionary.save('dictionary.gensim')

        
        self.model = gensim.models.LdaModel(corpus, num_topics = NUM_TOPICS, id2word=self.dictionary)
        self.model.save('model10.gensim')

        self.topics = self.model.print_topics(num_words=10)

    def get_topic_list(self, thread):
        line = self.concat_thread(thread)
        line = self.clean_text(line)
        bow = self.dictionary.doc2bow(line)
        
        topics = self.model.get_document_topics(bow)
        return topics
        #print(l)




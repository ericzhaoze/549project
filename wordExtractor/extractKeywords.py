import string
import math
import nltk

from nltk.tokenize import wordpunct_tokenize
from enum import Enum

from itertools import groupby, product, chain

from collections import Counter

class Metric(Enum):
    DEGREE_AND_FREQUENCY = 0
    WORD_DEGREE = 1
    WORD_FREQUENCY = 2
    POSITIVE_DOCUMENT_FREQUENCY = 3

class Rake(object):
    def __init__(self, maxlength = 30, language='english', metric = Metric.DEGREE_AND_FREQUENCY):
        #parameters
        self.metric = metric
        self.stopwords = nltk.corpus.stopwords.words(language)
        self.punctuations = string.punctuation
        self.ignore = set(chain(self.stopwords, self.punctuations))
        self.maxlength = maxlength


        #results
        self.frequency_map = None
        self.degree = None
        self.rank_list = None
        self.normalized_list = None
        self.ranked_phrases = None

        #new features
        self.document_frequency = None

    def get_ranked_phrase(self):
        return self.ranked_phrases

    def get_ranked_phrase_with_score(self):
        return self.rank_list

    def get_balanced_score(self):
        return self.normalized_list

    def get_frequency_map(self):
        return self.frequency_map

    def get_degrees(self):
        return self.degree
        
    #input: text chunk
    def extract_keywords(self, text):
        sentences = nltk.tokenize.sent_tokenize(text)
        phrases = self.generate_phrases(sentences)

        self.frequency_map = Counter(chain.from_iterable(phrases))

        self.document_frequency = dict()


        coOccurMap = dict()

        for phrase in phrases:
            for idx, sentence in enumerate(sentences):
                if phrase not in self.document_frequency:
                    self.document_frequency[phrase] = []
                size = len(self.document_frequency[phrase])
                if size == 0 or self.document_frequency[phrase][size-1] != idx:
                    self.document_frequency[phrase].append(idx
                    )
            for (word, coword) in product(phrase, phrase):
                if word not in coOccurMap:
                    coOccurMap[word] = dict()
                if coword not in coOccurMap[word]:
                    coOccurMap[word][coword] = 0
                coOccurMap[word][coword] += 1

        self.degree = dict()

        for key in list(coOccurMap.keys()):
            self.degree[key] = sum(list(coOccurMap[key].values()))


        self.rank_list = []
        for phrase in phrases:
            rank = 0.0
            for word in phrase:
                if self.metric == Metric.DEGREE_AND_FREQUENCY:
                    rank += float(self.degree[word]) / self.frequency_map[word]
                elif self.metric == Metric.WORD_FREQUENCY:
                    rank += float(self.frequency_map[word])
                elif self.metric == Metric.POSITIVE_DOCUMENT_FREQUENCY:
                    rank += float(self.frequency_map[word])
                else:
                    rank += float(self.degree[word])

            if self.metric == Metric.POSITIVE_DOCUMENT_FREQUENCY:
                rank = math.log(rank / float(len(self.document_frequency[phrase])))
            self.rank_list.append((rank, ' '.join(phrase)))
        self.rank_list.sort(reverse=True)
        
        self.normalized_list = []
        listsum = 0.0
        
        for word in self.rank_list:
            listsum += math.sqrt(math.sqrt(word[0]))
        for word in self.rank_list:
            newitem = (math.sqrt(math.sqrt((word[0])))/listsum, word[1])
            self.normalized_list.append(newitem)
        
        self.ranked_phrases = [p[1] for p in self.rank_list]


    def generate_phrases(self, sentences):
        phrases = set()

        for sentence in sentences:
            words = [word.lower() for word in wordpunct_tokenize(sentence)]
            phrases.update(self.generate_phrase_from_words(words))
        return phrases


    def generate_phrase_from_words(self, words):
        groups = groupby(words, lambda x : x not in self.ignore)
        phrases = [tuple(group[1]) for group in groups if group[0]]
        return list(
            filter(
                lambda x: len(x) <= self.maxlength, phrases
            )
        )

        return phrases


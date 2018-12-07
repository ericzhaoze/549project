import extractKeywords
from readRada import readFiles
from topicModeling import ModelGenerator
from select_keywords_related import select_keywords_related
import gensim.downloader as api
from collections import Counter


class ExtractManager(object):
    def __init__(self, trainDir, testDir, model):
        trainThreads, trainFiles = readFiles(trainDir)
        testThreads, testFiles = readFiles(testDir)

        # Load pre-trained model
        # print("Loading pretrained model...")
        # model = {}
        self.model = model
        # print("Model loaded.")

        tests = []
        for thread in testThreads:
            tests.append(self.concat_thread(thread))


        rake = extractKeywords.Rake(metric = extractKeywords.Metric.DEGREE_AND_FREQUENCY)
        topicmodel = ModelGenerator(trainThreads)

        self.rake = rake
        self.topicModel = topicmodel
        self.trainThreads = trainThreads
        self.testThreads = tests

    def concat_thread(self, thread):
        string = ''
        for line in thread:
            string += line
        return string

    def normalize_dictionary_values(self, outputlist):
        #print(outputlist)
        dsum = 0.0
        outputdict = {}

        for item in outputlist:
            outputdict[item[0]] = item[1]

        for key in list(outputdict.keys()):
            dsum += outputdict[key]

        newdict = {}
        for key in list(outputdict.keys()):
            newdict[key] = float(outputdict[key] / dsum)

        max_weight = float(newdict[outputlist[0]])
        min_weight = float(newdict[outputlist[len(outputlist) - 1]])

        for key in list(outputdict.keys()):
            newweight = (newdict[key] - min_weight) / (max_weight - min_weight) * 40.0 + 20
            newdict[key] = newweight


        return newdict


    def output_serializer(self, outputdict):
        print(outputdict)
        newdict = self.normalize_dictionary_values(outputdict)
        string = '['
        for key in list(newdict.keys()):
            string += '{\"text\":\"'
            string += str(key)
            string += '\",\"size\":'
            string += str(newdict[key])
            string += '},'
        size = len(string)
        string = string[:-1] + ']'
        return string


    def extract_keywords(self, topic_words = None, threads = None, keyword_number = 10):
        if threads == None:
            threads = self.testThreads

        keyword_for_threads = {}

        for idx, thread in enumerate(threads):
            if topic_words == None:
                topics = self.topicModel.get_topic_list(thread)
                toplist_candidate = self.topicModel.get_topics()
            else:
                topics = [(0,1)]
                words = topic_words.split()
                n = len(words)
                topic_words = ''
                for word in words:
                    topic_words += str(1.0/n) + '*"' + word + '" + '
                topic_words = topic_words[:-3]
                # print(topic_words)

                toplist_candidate = [(0,topic_words)]

            thread_keywords = []
            
            self.rake.extract_keywords(thread)
            words = self.rake.get_balanced_score()
            thread_keywords.append(words)
            #print('------------------------------------------')
            #print(files[idx])
            #print(email)
            #print(words)
            #print('------------------------------------------')
            
            print(thread_keywords)
            print('------------------------------------------')

            for top in topics:
                # print(top)
                topic_weight = top[1]
                topic_words = toplist_candidate[top[0]][1]
                keywords = select_keywords_related(self.model, thread_keywords, topic_words, keyword_number)
                # keyword_for_threads.update(keywords)
                for k, v in keywords:
                    if k in keyword_for_threads:
                        keyword_for_threads[k] += v * topic_weight
                    else:
                        keyword_for_threads[k] = v * topic_weight

            keyword_for_threads_counter = Counter(keyword_for_threads)

        return keyword_for_threads_counter.most_common(keyword_number)



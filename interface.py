import extractKeywords
from readRada import readFiles
from topicModeling import ModelGenerator
from select_keywords_related import select_keywords_related

class ExtractManager(object):
    def __init__(self, trainDir, testDir):
        trainThreads, trainFiles = readFiles(trainDir)
        testThreads, testFiles = readFiles(testDir)

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

    def extract_keywords(self, threads = None, keyword_number = 10):
        if threads == None:
            threads = self.testThreads

        keyword_for_threads = []

        for idx, thread in enumerate(threads):
            topics = self.topicModel.get_topic_list(thread)
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
                topic_words = self.topicModel.get_topics()[top[0]][1]
                keywords = select_keywords_related(thread_keywords, topic_words, keyword_number)
                keyword_for_threads.append(keywords)
        return keyword_for_threads
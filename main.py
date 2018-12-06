import extractKeywords
from readRada import readFiles
from topicModeling import ModelGenerator




def main():

    threads, files = readFiles('EmailSummarizationKeywordExtraction/small_test/')
    
    rake = extractKeywords.Rake(metric = extractKeywords.Metric.DEGREE_AND_FREQUENCY)
    topicmodel = ModelGenerator(threads)


    for idx, thread in enumerate(threads):
        #print(topics)
        #print(thread)
        topics = topicmodel.get_topic_list(thread)
        print(thread)
        for top in topics:
            print(top[1])
            print(topicmodel.get_topics()[top[0]])

        for email in thread:
            rake.extract_keywords(email)
            words = rake.get_ranked_phrase_with_score()
            #print('------------------------------------------')
            #print(files[idx])
            #print(email)
            #print(words)
            #print('------------------------------------------')

main()
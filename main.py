import extractKeywords
from readRada import readFiles
from topicModeling import ModelGenerator
from select_keywords_related import select_keywords_related


def main():

    threads, files = readFiles('EmailSummarizationKeywordExtraction/small_test/')
    
    rake = extractKeywords.Rake(metric = extractKeywords.Metric.DEGREE_AND_FREQUENCY)
    topicmodel = ModelGenerator(threads)


    for idx, thread in enumerate(threads):
        #print(topics)
        #print(thread)
        topics = topicmodel.get_topic_list(thread)
        # print(thread)
        # print('------------------------------------------')

        thread_keywords = []
        for email in thread:
            rake.extract_keywords(email)
            words = rake.get_ranked_phrase_with_score()
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
            topic_words = topicmodel.get_topics()[top[0]][1]
            select_keywords_related(thread_keywords, topic_words)


if __name__ == '__main__':
    main()
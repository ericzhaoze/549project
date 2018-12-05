import extractKeywords
from readRada import readFiles


def concat_thread(texts):
    string = ''
    for line in texts:
        string += line
    return string

def main():

    threads, files = readFiles('EmailSummarizationKeywordExtraction/small_test/')
    
    rake = extractKeywords.Rake(metric = extractKeywords.Metric.POSITIVE_DOCUMENT_FREQUENCY)
    
    for idx, thread in enumerate(threads):
        #print(thread)
        for email in thread:
            rake.extract_keywords(email)
            words = rake.get_ranked_phrase()
            print('------------------------------------------')
            #print(files[idx])
            print(email)
            print(words)
            print('------------------------------------------')

main()
import interface


test_input_thread = []
test_input_thread.append('I like hamburgers. I want to eat some now.\n' + ' I also like dogs, but not cats because they are too lazy.\n' + ' Can you feed my dog with a hamburger?')
test_str = "food"

def main():

    trainDir = 'EmailSummarizationKeywordExtraction/CorporateSingleXML/'
    testDir = 'EmailSummarizationKeywordExtraction/smallTest/'
    
    em = interface.ExtractManager(trainDir, testDir)
    # keywords1 = em.extract_keywords()
    # print(keywords1)

    keywords2 = em.extract_keywords(topic_words = test_str,threads = test_input_thread, keyword_number = 3)
    print(keywords2)


if __name__ == '__main__':
    main()
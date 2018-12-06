"""
A function to select keywords (already extracted) related to certain topic.

@ select_keywords_related.py
@ johson
@ 5 Dec, 2018
"""

import numpy as np
import nltk
import gensim.downloader as api
from collections import Counter


TOPNUM = 10

def calculate_simlar_score(vec, topic_vec, topic_weight):
	"Calculate similarity score based on word vector and topic vectors."
	score = []
	for i in range(len(topic_vec)):
		similar_score = np.dot(vec, topic_vec[i]) / (np.linalg.norm(vec) * np.linalg.norm(topic_vec[i]))
		score.append(similar_score * topic_weight[i])

	return np.sum(score)


def select_keywords_related(thread_keywords, topic_words):
	"Select keywords related to certain topic words."
	# Load pre-trained model
	print("Loading pretrained model...")
	# model = {}
	model = api.load("glove-twitter-25")
	print("Model loaded.")

	topic_related_scores = {}
	topic_weight = [float(topic.split('*')[0]) for topic in topic_words.split(' + ')]
	topic = [topic.split('*')[1].strip('"') for topic in topic_words.split(' + ')]
	# print(topic)

	topic_vec = [model[word] for word in topic]

	for i in range(len(thread_keywords)):
		for j in range(len(thread_keywords[i])):

			temp_score = []
			keyword_weight = thread_keywords[i][j][0]
			keywords = thread_keywords[i][j][1]

			for word in keywords.split():
				# print(word)
				try:
					vec1 = model[word]
					temp_score.append(keyword_weight * calculate_simlar_score(vec1, topic_vec, topic_weight))
				except Exception as e:
					temp_score.append(0)

			# Choose max related as the score
			topic_related_scores[keywords] = max(temp_score)

	# Choose top related keywords
	topic_related_scores_counter = Counter(topic_related_scores)
	print(topic_related_scores_counter.most_common(10))


# def main():
# 	"Main function."
# 	topic = ["food", "man", "work"]
# 	topic_weight = [0.6, 0.1, 0.3]
# 	thread_keywords = []
# 	thread_keywords.append(['vehicles per year', 'immediate family member', 'family twice', 'extended family', 'vpp program', 'vpp form', 'vehicles may', 'pass along savings', 'year', 'please let', 'infiniti dealers', 'hi carmen', 'anything else', 'affiliate companies', 'used', 'purchased', 'nna', 'nissan', 'need', 'limits', 'know', 'friends', 'employees', 'employee', '4', '2'])
# 	thread_keywords.append(['many extended family', '1 year', 'year', 'many', 'infiniti dealer', 'hi joan', 'form today', 'family', 'done one', 'used', 'use', 'think', 'thanks', 'received', 'questions', 'friends', 'forms', 'far', 'also'])
# 	select_keywords_related(thread_keywords, topic, topic_weight)


# if __name__ == '__main__':
# 	main()






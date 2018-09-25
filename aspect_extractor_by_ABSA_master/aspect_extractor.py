# encoding:utf8
import os,sys,re
import nltk
from nltk.collocations import *
from nltk.tokenize import *
from pos_tagger import *
import identify_entities
from feature_reduction import *
from feature_clustering import *
import pickle
import csv

bigram_measures = nltk.collocations.BigramAssocMeasures()
trigram_measures = nltk.collocations.TrigramAssocMeasures()

def convert_review_text_to_nltk_text(review_text):
	review_text = re.sub("[.':!?*&#]", " ", review_text)
	tokens = word_tokenize(review_text)
	return tokens

def get_collocations(nltk_text):
	finder = BigramCollocationFinder.from_words(nltk_text)
	finder.apply_freq_filter(3)
	collocations = finder.nbest(bigram_measures.pmi,20)
	# collocations = [' '.join(i) for i in collocations]
	# finder.score_ngrams(bigram_measures.pmi)
	# print collocations
	return collocations

# 这里reviewtext就是只前得到的从文件中read到的数据进行一些基础预处理
def analyse_one_product(review_text):
	# 只有句号一种标点符号，有大小写，是出于分句的考虑？
	review_text_copy = review_text
	review_text = ""
	for review in review_text_copy:
		review_text += review
	review_text = review_text.lower()
	features = []
	nltk_text = convert_review_text_to_nltk_text(review_text)
	collocations = get_collocations(nltk_text)
	# print("collections:")
	# for co in collocations:
	# 	print(co)
	Title = ''
	# review_text：全小写且进行过一些基础预处理的文本
	# Title没用到，返回频数足够的1，2，3元组合
	entities = identify_entities.main(review_text,Title)
	# 简易分词（利用nltk将不合适的组合抛弃），entities又变成元祖列表了
	entities = [tuple(word_tokenize(i)) for i in entities]
	# print("entities:")
	# for entry in entities:
	# 	print(entry)
	# reviews变成列表，每个是一个评论
	reviews = review_text_copy
	# 过滤分的短的...可能是符号之类的玩意
	reviews = [i for i in reviews if len(i) > 1]
	# 分句,返回包含多个句子的列表，变成双重列表
	review_text_tokenized = [sent_tokenize(review) for review in reviews]
	# nouns，verbs，adjectives，adverbs：（单词，评论数，句子数），candidate_sentences（评论数， 句子数，（adj，n）），collocation_tagged，entities_tagged：合格的组合（组合，True）
	nouns,verbs,adjectives,adverbs,candidate_sentences,collocation_tagged,entities_tagged = pos_tagger(review_text_tokenized,collocations,entities)
	# print("candidate_sentences")
	# for i in candidate_sentences:
	# 	print(i[2])
	features = feature_reduction(collocation_tagged,candidate_sentences,entities_tagged, review_text_tokenized)
	features = cluster_features(features)
	feature_list = [i for i in features]
	return feature_list,features

def test_cwd():
	print(os.getcwd())



import os
import pandas as pd
from data_process import DataProcess
from text_preprocess import text_preprocess
import json
import numpy as np
from aspect_extractor import test_cwd
from functions import get_attrs_from_dicts

# attrs = []
# get_attrs_from_dicts({"a":"er", "b":{"c":"f", "f":"r"}, "r":"e", "q":[{"c":"m", "t":"o"}]}, attrs=attrs)
# print(attrs)


# path = "H:\Electronics_extraction\get_aspects_like_ABSA/test.txt"
# print(os.path.splitext(path)[1])

df = pd.DataFrame({"key":[1,2,1,4,np.nan], "value": [3,4,6,2, np.nan], "id": [3,5,6,7,0], "names":["", "dawda", "wadad", "", "wvas"]})
# print(df)
# gb = df.groupby("key")
# for name, group in gb:
# 	print(name)
# 	print(group)
# print("key" in df.columns)
# .values.tolist()
# print(type(df["value"]) == pd.Series)
# print(df[["key"]])
# print(pd.DataFrame([df["key"].describe(), df["value"].describe()]))
# print(type(df["key"].value_counts()))
# print(df["key"][0])
# print(str(df["key"].dtype).startswith("float"))
# print(df[["key", "id"]])
# print(df["names"].dropna())
# df = df[(True - df["name"].isin([""]))]
# print(df[df["names"].isin([""])])


# getcwd（）方法获得的结果是运行时的代码位置
# test_cwd()

# list = []
# if not list:
# 	print("nice!")

dp = DataProcess()
# df = dp.to_data_frame("./testData/test.json")
# dp.group_data_by_attr_value("asin", grouped_attrs=["reviewText"], save_to_dir="./testData/reviews_by_asin", read_only=True)
# dp.filter_attrs("reviewText")
# dp.get_statics(["reviewerID", "asin"], show_axis=0, show_details=True)
# dp.get_reviews_aspect("we")
# dp.save_to_file("test.json", csv_type=False)
# final_aspect = dp.get_reviews_aspect("reviewText", "Cell_Phones")
# with open("./data/test_final.json", 'a') as f:
# 	for tag in final_aspect:
# 		print(tag+":"+str(final_aspect[tag]))
# 		f.write(json.dumps(final_aspect[tag]) + "\n")
# df = dp.to_data_frame("./data/test_final.json")
# dp.get_statics(["user_id", "item_id"], df=df, show_details=True)
# df = dp.to_data_frame("H:/from qq\MobileFile/yelp_academic_dataset_restaurant_state_review_spi.csv")
# df = df.drop(subset=["reviewText"])
# print(df)
# print(df["review"])
# final_aspect = dp.get_reviews_aspect(review_attr_name="review", df=df, group_attr="restaurant_id", keeped_attrs={"restaurant_id":"restaurant_id","user_id":"name","stars":"stars"})
# with open("./data/yelp_final.json", 'a') as f:
# 	for tag in final_aspect:
# 		print(tag+":"+str(final_aspect[tag]))
# 		f.write(json.dumps(final_aspect[tag]) + "\n")
# dp.build_corpus_for_datas(df, review_attr="reviewText", corpus_type="test")
# dp.build_dictionry_for_final_aspects("./data/test_final.json", dictionary_attrs=["user_id", "item_id"])
# df = dp.to_data_frame("test_cell_phone.json")
# final_aspect = dp.get_reviews_aspect("reviewText", "Cell_Phones", {"user_id":"reviewerID", "item_id": "asin", "stars": "overall"}, group_attr="asin", df=df, save_to_file="amazon_final.json")
# UnicodeDecodeError: 'utf-8' codec can't decode byte 0xd4 in position 1: invalid continuation byte

# TODO:在collections中去掉非名词的，去掉‘ ，在提取collections中去掉 . ，加上not进行考虑

# def get_the_final_aspects(file):
# 	df = dp.to_data_frame(file=file)
# 	final_aspect = dp.get_reviews_aspect("reviewText", "Cell_Phones", {"user_id":"reviewerID", "item_id": "asin", "stars": "overall"}, group_attr="asin", df=df, save_to_file="cell_phone_final_aspects.json")

# get_the_final_aspects("H:\Electronics_extraction\Data/Cell_Phones_and_Accessories_5.json")

# 统计原数据的数量
# df = dp.to_data_frame("H:\Electronics_extraction\Data/Cell_Phones_and_Accessories_5.json")
# dp.get_statics(["reviewerID"],df=df)
# 194439 / 44090

# def static_final_wrong(file):
# 	count = 0
# 	total = 0
# 	with open(file, 'r') as f:
# 		data = f.readline()
# 		while data:
# 			data_json = json.loads(data)
# 			sentiment = 0
# 			for aspect in data_json["aspect"]:
# 				for senti in data_json["aspect"][aspect]:
# 					sentiment += float(senti["sentiment"])
# 			if sentiment > 0 and data_json["stars"] < 3:
# 				count += 1
# 			elif sentiment < 0 and data_json["stars"] > 3:
# 				count += 1
# 			total += 1
# 			data = f.readline()
# 	print("count:"+str(count)+"\ttotal:"+str(total))
# # count:818	total:4690
# static_final_wrong("H:\DataPreprocess\data_process\data/amazon_final.json")

# df = dp.to_data_frame("H:/from qq\MobileFile/yelp_academic_dataset_restaurant_state_review_spi.csv")
# df = dp.to_data_frame("test_yelp.csv")
# dp.save_to_file("test_yelp_test.csv", df=df, csv_type=False)
# df = dp.filter_attrs(["restaurant_id", "name"], df=df)
# df = dp.reform_attrs({"tag":["restaurant_id", "stars"]}, df=df)
# df = df.rename(columns={"stars":"overall"})
# df = dp.group_data_by_attr_value("name", df=df, values=["UqYtHGxXJK9s4ltIm6Uw_w", "0pf5VuzE4_1pwj5NJHG5TQ"], grouped_attrs=["name", "restaurant_id"], gather=False, save_to_dir="test_group")
# df1, df2 = dp.splite_data(df=df, extract_dep_attr="name")
# print(df1)
# print(df2)
# dp.get_relations("name", "stars", df=df)
# dp.get_statics(["name"], df=df, show_details=True)

# def cut_data(file1, file2):
# 	i = 0
# 	with open(file1) as f1, open(file2, 'a') as f2:
# 		data = f1.readline()
# 		while data:
# 			i += 1
# 			f2.write(data.strip()+"\n")
# 			data = f1.readline()
# 			if i >= 20000:
# 				break
# cut_data("H:\Electronics_extraction\Data/Cell_Phones_and_Accessories_5.json", "./data/test_cell_phone.json")
# cut_data("H:/from qq\MobileFile/yelp_academic_dataset_restaurant_state_review_spi.csv", "./data/test_restaurant.csv")

# final_aspect = dp.get_reviews_aspect("review", "restaurant", df=df, group_attr="restaurant_id", keeped_attrs={"restaurant_id":"restaurant_id","user_id":"name","stars":"stars"}, save_to_file="test_final.json")
# with open("./data/test_final.json", 'a') as f:
# 	for tag in final_aspect:
# 		print(tag+":"+str(final_aspect[tag]))
# 		f.write(json.dumps(final_aspect[tag]) + "\n")


# obj = {'restaurant_id': '-01XupAWZEXbdNbxNg5mEg', 'user_id': 'fi4D4qlRmLgNkHr4GZusgw', 'stars': 5, 'aspect': {'restaurant': [{'opinion': 'warm', 'sentiment': '0.625'}], 'food': [{'opinion': 'good', 'sentiment': '1.0'}]}}
# print(json.dumps(obj))


# from nltk.corpus import stopwords
# english_stopwords=set(stopwords.words('english'))
# print(english_stopwords)

# str = "I could only give this USB car \ncharger 2 stars because although it worked fine for about 3 months, \nit subsequently died on me.Pros:-Has 2 USB ports for charging, one (the top) is 2.1 amps.  The bottom slot is lower, presumably 1 or 1.5 amps.-Fits well in my charging socket - holds tight.  I've had some that were loose in my charging socket.-Works well to charge my iPhone in the top slot and the bottom slot works with most Android phones, except the very high end ones.-Has a blue LED light to tell you it is on and ready to charge.-The USB sockets seem to be well made and tightly fit all my cables.-Pretty solid construction.-It cost less than $2.Cons:-It died on me after 3 months.I had really enjoyed using this USB charger.  It rapidly charged my iPhone and worked well with charging the phones of my family and friends.  The two slot design makes this design very handy; with a 1 slot design, no one else can charge their device unless I remove my cord.  Of course, after this charger died, I had to go back to the 1 slot design I was using before.After 3 months, I began to notice the LED light flickering.  It was less than a week later that is quit working permanently.  I'm not sure what the problem was - faulty wiring, bad design, I guess I'll never know.  I thought about getting another since they are so cheap, but then I thought better of it.  Maybe they are so cheap because they are simply disposable after a short period of time.For whatever reason, it died and I was forced to look for another 2 slot design - I haven't found one in my price range yet."
# print(text_preprocess(str))

# from nltk.corpus import sentiwordnet as swn
#
# d = {}
#
# def maxi(ls):
# 	if len(ls) == 0:
# 		return 0
# 	else:
# 		return max(ls)
#
# def get_score(adjective):
# 	if adjective not in d:
# 		scores = list(swn.senti_synsets(adjective))
# 		pos_scores = [i.pos_score() for i in scores]
# 		neg_scores = [i.neg_score() for i in scores]
# 		obj_scores = [i.obj_score() for i in scores]
# 		pos_score = maxi(pos_scores)
# 		neg_score = maxi(neg_scores)
# 		obj_score = maxi(obj_scores)
# 		if len([x for x in scores]) == 0:
# 			print("every time?!")
# 			d[adjective] = (-1,-1,-1,-1,-1,-1)
# 			return (-1,-1,-1,-1,-1,-1)
# 		scores_ad = swn.senti_synsets(adjective,pos='ar')
# 		pos_scores_ad = [i.pos_score() for i in scores_ad]
# 		neg_scores_ad = [i.neg_score() for i in scores_ad]
# 		obj_scores_ad = [i.obj_score() for i in scores_ad]
# 		pos_score_ad = maxi(pos_scores_ad)
# 		neg_score_ad = maxi(neg_scores_ad)
# 		obj_score_ad = maxi(obj_scores_ad)
# 		d[adjective] = (pos_score,neg_score,obj_score,pos_score_ad,neg_score_ad,obj_score_ad)
# 	else:
# 		(pos_score,neg_score,obj_score,pos_score_ad,neg_score_ad,obj_score_ad) = d[adjective]
# 	if pos_score == -1:
# 		return -100
# 	if pos_score_ad > neg_score_ad:
# 		return pos_score_ad
# 	elif pos_score_ad < neg_score_ad:
# 		return -neg_score_ad
# 	elif pos_score > neg_score:
# 		return pos_score
# 	elif pos_score < neg_score:
# 		return -neg_score
# 	else:
# 		return 0
#
# print(get_score("low"))



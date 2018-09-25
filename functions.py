# encoding:utf8
import pandas as pd
import json
from nltk.corpus import wordnet
import re
from collections import Iterable

from tools import *



# 在类使用中用到的方法模块，亦可单独提出使用
def json_to_csv(filename, filename_to, trans_forms):
	# df_dict格式
	df_dict = {}
	for attr in trans_forms:
		df_dict[attr] = []
	# 打开文件逐行遍历合并数据
	with open(filename, 'r') as f:
		data = f.readline()
		while data:
			data_json = json.loads(data)
			if data_json["reviewText"] != "":
				for attr in trans_forms:
					temp = ""
					if type(trans_forms[attr]) == list:
						for i in trans_forms[attr]:
							if temp != "":
								temp += '-'
							temp += data_json[i]
					else:
						temp = data_json[trans_forms[attr]]
					df_dict[attr].append(temp)
			data = f.readline()
	# 建立df_dict并写入文件，文件名为原文件名加 _csv
	df = pd.df_dict(df_dict)
	df.to_csv(filename_to, index=False)


def trans_json_to_data_frame(file, columns=[]):
	df_dict = {}
	# 获取json的keys
	headers = get_json_headers(file)
	# 声明一个dataFrame格式的字典
	for header in headers:
		df_dict[header] = []
	with open(file, 'r') as f:
		data = f.readline()
		while data:
			data = json.dumps(eval(data))
			data_json = json.loads(data)
			for header in headers:
				try:
					df_dict[header].append(data_json[header])
				except KeyError:
					df_dict[header].append("")
			data = f.readline()
	df = pd.DataFrame(df_dict)
	return df


def get_attrs_from_dicts(data, attrs):
	if isinstance(data, Iterable):
		if type(data) == dict:
			for attr in data:
				attrs.append(attr)
				if isinstance(data[attr], Iterable):
					attrs = get_attrs_from_dicts(data[attr], attrs)
		elif type(data) == list:
			for attr in data:
				if isinstance(attr, Iterable):
					attrs = get_attrs_from_dicts(attr, attrs)
	return attrs


def build_dictionry_for_final_aspects(file, dictionary_attrs=[]):
	attr_values = {}
	with open(file) as f:
		data = f.readline()
		data_json = json.loads(data)
		for attr in dictionary_attrs:
			if attr not in data_json:
				print(attr + u"不在文件里！")
				return
			attr_values[attr] = set()
		attr_values["aspect"] = set()
		attr_values["opinion"] = set()
		while data:
			for attr in dictionary_attrs:
				attr_values[attr].add(data_json[attr])
			for aspect in data_json["aspect"]:
				attr_values["aspect"].add(aspect)
				for opinions in data_json["aspect"][aspect]:
					attr_values["opinion"].add(opinions["opinion"])
			data = f.readline()
			try:
				data_json = json.loads(data)
			except:
				print(u"文件已读完！")
	for attr in attr_values:
		attr_list = list(attr_values[attr])
		if not os.path.exists(os.path.join(os.getcwd(), "dictionarys")):
			os.mkdir(os.path.join(os.getcwd(), "dictionarys"))
		save_to_dict(os.path.join(os.getcwd(), "dictionarys/"+attr+"_dict.txt"), attr_list)
	return





















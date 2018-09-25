# encoding:utf8
import pandas as pd
import numpy as np
import os, sys, stat
import csv
from nltk.corpus import stopwords

from tools import *
from functions import *
from aspect_extractor_by_ABSA_master.aspect_extractor import analyse_one_product
from text_preprocess import text_preprocess
from aspect_extractor_by_ABSA_master.feature_reduction import set_text

stopwords = set(stopwords.words('english'))

# 一个用来进行数据处理的主类,以dataframe为核心
class DataProcess():

	def __init__(self, file=""):
		'''
		类中可能会用来存放关于文件的统计信息等
		:param file:
		'''
		file = self.get_file_format(file)
		if not os.path.isfile(file):
			self.file=""
		else:
			self.file=file
		self.df=pd.DataFrame()
		self.reviews_dir=""

	# 小工具，检验其他方法中输入的df
	def get_df_input_formated(self, df):
		if df.empty:
			if self.df.empty:
				if self.file != "":
					self.df = self.to_data_frame(file=self.file)
					df = self.df
				else:
					print(u"没有有效文件名或有效dataframe！")
					return pd.DataFrame()
			else:
				df = self.df
		return df

	def get_file_format(self, file):
		if os.path.isabs(file):
			return file
		else:
			if os.path.exists(os.path.join(os.getcwd(), "data")):
				if os.path.exists(os.path.join(os.getcwd(), "data", file)):
					return os.path.join(os.getcwd(), "data", file)
			else:
				if os.path.exists(os.path.join(os.getcwd(), file)):
					return os.path.join(os.getcwd(), file)
				else:
					print(u"无法在当前路径和data文件夹下定位到文件！")
					return ""

	# TODO；test
	# 将数据转化为pandas的dataFrame格式
	def to_data_frame(self, file="", save_to_file=""):
		file = self.get_file_format(file)
		if file == "" and self.file == "":
			print(u"缺少有效文件名！")
			return
		if file == "":
			file = self.file
		file_type = get_file_type(file)
		# 根据文件类型采用不同方法获得pandas的dataFrame结构
		if file_type == ".csv":
			df = pd.read_csv(file)
		elif file_type == ".json":
			df = trans_json_to_data_frame(file)
		else:
			print(u"尚不支持此类数据集！")
			return
		# 判断保存文件参数是否可用
		if save_to_file != "":
			if os.path.isabs(save_to_file):
				df.to_csv(save_to_file, index=False)
			else:
				if not os.path.exists(os.path.join(os.getcwd(), "data")):
					os.mkdir(os.path.join(os.getcwd(), "data"))
				df.to_csv(os.path.join(os.getcwd(), "data", save_to_file), index=False)
		return df

	# 将df保存到文件中，默认为csv格式，否则为json
	def save_to_file(self, path, df=pd.DataFrame(), csv_type=True):
		df = self.get_df_input_formated(df)
		if df.empty:
			return
		if not os.path.isdir(os.path.dirname(path)):
			if not os.path.isdir(os.path.join(os.getcwd(), "data")):
				os.mkdir(os.path.join(os.getcwd(), "data"))
				path = os.path.join(os.getcwd(), "data", path)
			else:
				path = os.path.join(os.getcwd(), "data", path)
		if csv_type:
			df.to_csv(path, index=False)
		else:
			with open(path, 'a') as f:
				for data in json.loads(df.to_json(orient='records')):
					# print(data)
					f.write(json.dumps(data) + "\n")

	def rename_columns(self, df=pd.DataFrame(), new_names=[], new_old_names={}):
		df = self.get_df_input_formated(df)
		if df.empty:
			return
		if new_names:
			if len(new_names) != len(df.columns):
				print(u"参数new_names长度与dataframe不匹配!")
				return
			df.columns = new_names
			# df.rename(columns=new_names)
			return df
		if new_old_names:
			df.rename(columns=new_old_names)
			return df

	# 过滤掉非指定的属性值
	def filter_attrs(self, attrs_keeped, df=pd.DataFrame()):
		df = self.get_df_input_formated(df)
		if df.empty:
			return
		if type(attrs_keeped) != list:
			print(u"filter_attr中保留项的格式限定为列表.")
			return
		if not attrs_keeped:
			print(u"filter_attr中保留项不能为空！")
			return
		df = df[attrs_keeped]
		return df

	# 按对应的格式对df的列进行重新组织，合并列或者重命名
	# reform_dict = {"new_name": ["old_name1", "old_name2"], "new_name2": "old_name3"}
	def reform_attrs(self, reform_dict, df=pd.DataFrame(), only_dict_attrs=False):
		df = self.get_df_input_formated(df)
		if df.empty:
			return
		new_names = {}
		for attr in reform_dict:
			if type(reform_dict[attr]) == list:
				df[attr] = ""
				# print(attr, df.columns)
				for old_attr in reform_dict[attr]:
					if old_attr not in df.columns:
						print(old_attr + u"不是df的属性！")
						return
					if "int" in str(df[old_attr].dtype) or "float" in str(df[old_attr].dtype):
						df[old_attr] = df[old_attr].astype(str)
					if df[attr].all() == "":
						df[attr] = df[old_attr]
						del df[old_attr]
					else:
						df[attr] = df[attr].str.cat(df[old_attr], sep="-")
						# df[attr] += "-" + df[old_attr]
						del df[old_attr]
			else:
				if reform_dict[attr] not in df.columns:
					print(reform_dict[attr] + u"不是df的属性！")
					return
				new_names[reform_dict[attr]] = attr
		df = df.rename(columns=new_names)
		names = list(df.columns)
		new_name = []
		for name in reform_dict:
			new_name.append(name)
		if not only_dict_attrs:
			for name in names:
				if name not in reform_dict:
					new_name.append(name)
		df = df[new_name]
		return df

	# 以指定的属性将数据集进行提取
	def group_data_by_attr_value(self, attr, df=pd.DataFrame(), value="", values=[], gather=False, grouped_attrs=[], save_to_dir="", save_as_pickle=False, read_only=True):
		df = self.get_df_input_formated(df)
		if df.empty:
			return
		if attr not in df.columns:
			print(attr + u"不是数据集的key！")
			return
		if not values:
			values = values
		if value != "":
			values = [value]
		groups_dict = {}
		groups = df.groupby(attr)
		if values:
			# for name, group in groups:
			# 	group = group.reset_index()
			# 	if name in values:
			# 		if grouped_attrs:
			# 			group = group[grouped_attrs]
			# 		groups_dict[name] = group
			# 		values.remove(name)
			# 		if not values:
			# 			break
			# TODO: test!
			for value in values:
				groups_dict[value] = groups.get_group(value)
				groups_dict[value] = groups_dict[value]
		else:
			for name, group in groups:
				group = group.reset_index()
				if grouped_attrs:
					group = group[grouped_attrs]
				groups_dict[name] = group
		if grouped_attrs:
			for attr in grouped_attrs:
				if attr not in df.columns:
					print(attr + u"不在属性中！不予考虑")
					grouped_attrs.remove(attr)
			for name in groups_dict:
				groups_dict[name] = groups_dict[name][grouped_attrs]
		if gather:
			# new_df = pd.DataFrame()
			# for name in groups_dict:
			# 	print(groups_dict[name])
			# 	new_df = new_df.append(groups_dict[name], ignore_index=True)
			new_df = pd.concat(list(groups_dict.values()), ignore_index=True)
			groups_dict = new_df
		if save_to_dir != "":
			if not os.path.isabs(save_to_dir):
				if not os.path.exists(os.path.join(os.getcwd(), "data")):
					os.mkdir(os.path.join(os.getcwd(), "data"))
				if not gather:
					if not os.path.isdir(os.path.join(os.getcwd(), "data", save_to_dir)):
						os.mkdir(os.path.join(os.getcwd(), "data", save_to_dir))
				save_to_dir = os.path.join(os.getcwd(), "data", save_to_dir)
		if save_to_dir != "":
			if not gather:
				for name in groups_dict:
					if save_as_pickle:
						pd.to_pickle(groups_dict[name], os.path.join(save_to_dir, "._"+name+".csv"))
						if read_only:
							os.chmod(os.path.join(save_to_dir, "._"+name+".csv"), stat.S_IREAD)
					else:
						groups_dict[name].to_csv(os.path.join(save_to_dir, name+".csv"), index=False)
						if read_only:
							os.chmod(os.path.join(save_to_dir, name+".csv"), stat.S_IREAD)
			else:
				new_df.to_csv(save_to_dir, index=False)
				if read_only:
					os.chmod(save_to_dir, stat.S_IREAD)
		return groups_dict

	# 对数据集进行整体统计，展示数据总数，某些列的数目的统计结果，将结果自高到低展示并可视化
	def get_statics(self, attrs, df=pd.DataFrame(), show_axis=1, show_details=False, save_to_file="", draw_picture=False):
		df = self.get_df_input_formated(df)
		if df.empty:
			return
		if type(attrs) != list:
			print(u"参数attrs要求格式为列表！")
		if show_axis:
			describes = {}
			for attr in attrs:
				describes[attr] = (df[attr].describe())
			print(pd.DataFrame(describes))
		else:
			describes = []
			for attr in attrs:
				describes.append(df[attr].describe())
			print(pd.DataFrame(describes))
		if show_details:
			details = []
			for attr in attrs:
				details.append(df[attr].value_counts())
			for detail in details:
				print(detail)
				print(detail.describe())

	def fliter_data(self, df=pd.DataFrame(), attrs=["reviewText"]):
		df = self.get_df_input_formated(df)
		if df.empty:
			return
		for attr in attrs:
			if not str(df[attr].dtype).startswith("float") or not str(df[attr].dtype).startswith("int")or not str(df[attr].dtype).startswith("double"):
				# df = df[(True - self.df[attr].isin([""]))]
				df.drop(subset=attr)
			else:
				df = df.dropna(axis=0, subset=[attr])
		return df

	def splite_data(self, extract_dep_attr, df=pd.DataFrame(), extract_persent=0.6):
		df = self.get_df_input_formated(df)
		if df.empty:
			return
		if extract_dep_attr != "":
			if extract_dep_attr not in df.columns:
				print(extract_dep_attr+u"不是df中的属性名！")
				return
		groups = df.groupby(extract_dep_attr)
		train_df = pd.DataFrame()
		test_df = pd.DataFrame()
		for name, group in groups:
			group = group.reset_index()
			nums = get_a_random_list(0, len(group), int(len(group) * extract_persent))
			anti_nums = [i for i in range(len(group)) if i not in nums]
			train_df = train_df.append(group.loc[nums], ignore_index=True)
			test_df = test_df.append(group.loc[anti_nums], ignore_index=True)
		return train_df, test_df

	def build_dictionry_for_final_aspects(self, file, dictionary_attrs):
		build_dictionry_for_final_aspects(file, dictionary_attrs)

	# TODO:废弃？
	def get_review_text_by_prodect(self, reviews_path):
		reviews_texts = []
		# asins = df["asin"].value_counts().index
		# for asin in asins:
		# 	with open(os.path.join(reviews_path, asin+".csv")) as f:
		# 		header = f.readline()
		# 		reviews_texts.append(f.read())
		text_files = os.listdir(reviews_path)
		if len(text_files) != 0:
			for file in text_files:
				with open(os.path.join(reviews_path, file)) as f:
					header = f.readline()
					reviews_texts.append(f.read())
		else:
			print(u"文件夹"+reviews_path+"中没有有效文件！")
		return reviews_texts

	# TODO: 依照频率进行属性过滤的相关方法书写

	def build_corpus_for_datas(self, df=pd.DataFrame(), review_attr="", corpus_type=""):
		corpus_review_nums = 1000
		if len(df[review_attr]) > corpus_review_nums:
			random_indexs = get_a_random_list(0, len(df[review_attr]), corpus_review_nums)
			review_series = list(df[review_attr][random_indexs])
			# print(df[review_attr][random_indexs])
			if os.path.isdir(os.path.join(os.getcwd(), "data")):
				with open(os.path.join(os.getcwd(), "data/General_Corpus_for_"+corpus_type), 'a') as f:
					for review in review_series:
						try:
							f.write(str(review)+"\n")
						except:
							print(u"有异常字符")
			os.chmod(os.path.join(os.getcwd(), "data/General_Corpus_for_"+corpus_type), stat.S_IREAD)
			print(u"语料库创建完成！")
			return os.path.join(os.getcwd(), "data/General_Corpus_for_"+corpus_type)
		else:
			print(u"总评论数不足，不需构建语料库！")
			return ""

	# 从数据集中获取评论的aspect和opinion，sentiment信息（未必所有的评论都有）
	#group_attr="asin" keeped_attrs = {"user_id": "reviewerID", "item_id": "asin", "stars": "overall"}
	def get_reviews_aspect(self, review_attr_name, corpus_type, keeped_attrs, group_attr="", df=pd.DataFrame(), reviews_path="", save_to_file=""):
		df = self.get_df_input_formated(df)
		if df.empty:
			return
		# 由于目前python中存在的bug：https://bugs.python.org/issue24313，np.int64无法dumps到字符串，所以提前将其改为float。。。
		for attr in keeped_attrs:
			if df[keeped_attrs[attr]].dtype == np.int64:
				# print(keeped_attrs[attr])
				df[keeped_attrs[attr]] = df[keeped_attrs[attr]].astype(float)
				# print(df[keeped_attrs[attr]].dtype)
		if save_to_file != "":
			if not os.path.isabs(save_to_file):
				if not os.path.exists(os.path.join(os.getcwd(), "data")):
					os.mkdir(os.path.join(os.getcwd(), "data"))
				save_to_file = os.path.join(os.getcwd(), "data", save_to_file)
			if os.path.exists(save_to_file):
				print(save_to_file + u"文件已存在！若要重新运行请先删除文件！")
		# df = self.fliter_data(df, [review_attr_name])
		if os.path.exists(os.path.join(os.getcwd(), "data/General_Corpus_for_"+corpus_type)):
			corpus = os.path.join(os.getcwd(), "data/General_Corpus_for_"+corpus_type)
		else:
			corpus = self.build_corpus_for_datas(df, review_attr=review_attr_name, corpus_type=corpus_type)
		# 设置文本语料库，做高频筛选
		if corpus != "":
			set_text(corpus)
		if group_attr != "":
			keeped_attrs_list = list(keeped_attrs.values())
			keeped_attrs_list.append(review_attr_name)
			# print(keeped_attrs_list)
			reviews_dfs = self.group_data_by_attr_value(group_attr, df=df,
														grouped_attrs=keeped_attrs_list)
			print(u"数据分组完成！")
		else:
			reviews_dfs = df[list(keeped_attrs.keys()).append(review_attr_name)]
		# print(reviews_dfs)
		final_aspect_opinion = {}
		count = 0
		total = len(reviews_dfs)
		for name in reviews_dfs:
			count += 1
			if count / 100 == 0:
				print(u"已运行"+str(count)+u"个条目！"+u"\t总条目："+str(total)+u"\t进度："+str(count/total))
			text = []
			for review in reviews_dfs[name][review_attr_name]:
				text.append(text_preprocess(review))
			feature_list, features = analyse_one_product(text)
			for feature in features:
				# print(features[feature])
				aspect = " ".join([word for word in feature if word not in stopwords])
				if aspect != "":
					for feature_detail in features[feature]:
						attr_values = {}
						tag_name = ""
						for attr in keeped_attrs:
							attr_values[attr] = reviews_dfs[name][keeped_attrs[attr]][feature_detail[0]]
							if "id" in attr:
								tag_name += (str(attr_values[attr]) + "-")
						tag_name = tag_name.strip("-")
						if tag_name not in final_aspect_opinion:
							one_review_msg = {}
							for attr in attr_values:
								one_review_msg[attr] = attr_values[attr]
							one_review_msg["aspect"] = {}
							one_review_msg["aspect"][aspect] = []
							one_review_msg["aspect"][aspect].append({"opinion": str(feature_detail[3]), "sentiment": str(feature_detail[2])})
							final_aspect_opinion[tag_name] = one_review_msg
						else:
							one_review_msg = final_aspect_opinion[tag_name]
							if aspect in one_review_msg["aspect"]:
								one_review_msg["aspect"][aspect].append(
									{"opinion": str(feature_detail[3]), "sentiment": str(feature_detail[2])})
							else:
								one_review_msg["aspect"][aspect] = []
								one_review_msg["aspect"][aspect].append(
									{"opinion": str(feature_detail[3]), "sentiment": str(feature_detail[2])})
		if save_to_file != "":
			with open(save_to_file, 'a') as f:
				for tag in final_aspect_opinion:
					f.write(json.dumps(final_aspect_opinion[tag]) + "\n")
		return final_aspect_opinion

	# TODO: test
	def get_relations(self, main_relation_attr, second_ralation_attr, df=pd.DataFrame()):
		relation_df = pd.DataFrame()
		df = self.get_df_input_formated(df)
		if df.empty:
			return
		relation_groups = self.group_data_by_attr_value(main_relation_attr, df=df, grouped_attrs=[])
		attrs = relation_groups.keys()
		relation_df.columns = attrs
		relation_df.indexs = attrs


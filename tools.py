# encoding:utf8
import os
import json
import random
import stat


# 返回一个包含首尾的随机数列
def get_a_random_list(start, end, nums, repeat=False, typeInt=True):
	list = []
	if end < start:
		(head, tail) = (end, start)
	else:
		(head, tail) = (start, end)
	if typeInt:
		if not repeat:
			if tail - head + 1 < nums:
				print(u"nums has been biger than all the nums!")
				return None
			for i in range(nums):
				num = random.randint(head, tail)
				while num in list:
					num = random.randint(head, tail)
				list.append(num)
		else:
			for i in range(nums):
				list.append(random.randint(head, tail))
	else:
		if not repeat:
			for i in range(nums):
				num = random.uniform(head, tail)
				while num in list:
					num = random.uniform(head, tail)
				list.append(num)
		else:
			for i in range(nums):
				list.append(random.uniform(head, tail))
	return list


# 服务于功能模块的工具集合
def get_json_headers(file):
	headers = []
	with open(file, 'r') as f:
		data = f.readline()
		data = json.dumps(eval(data))
		data = json.loads(data)
		for attr in data:
			headers.append(attr)
	return headers


def get_file_type(path):
	return os.path.splitext(path)[1]


def save_to_dict(file, list):
	with open(file, 'a') as f:
		for i,id in enumerate(list):
			f.write(str(i)+"\t"+id+"\n")
	os.chmod(file, stat.S_IREAD)


def load_from_dict(file, ID_to_num=True):
	dict = {}
	with open(file, 'r') as f:
		data = f.readline()
		datas = data.strip().split("\t")
		if ID_to_num:
			key = 1
		else:
			key = 0
		dict[datas[key]] = datas[abs(1-key)]
	return dict













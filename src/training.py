#!/usr/bin/python

from textblob.classifiers import NaiveBayesClassifier
from textblob import TextBlob
import os
import re
import sys
import pickle

train=[]
stopwords=[]
data=""
dataset_path="training/"
with open("stopwords", 'r') as infile:
	data = infile.read().replace("\n","")
folders = [folder for folder in os.listdir(dataset_path)]

stopwords=data.split(",")

for category in folders:
	print category
	os.chdir(dataset_path + category)
	for files in os.listdir('.'):
		with open(files, 'r') as my_file:
			data = my_file.read().lower()
			for stopword in stopwords:
				regex=r'\b'+re.escape(stopword)+r'\b'
				lowercase = re.compile(regex)
				data = lowercase.sub(r'', data)
			data=re.sub(r'[^\x00-\x7F]+','', data)
			data=re.sub(r'[\x21-\x2F]+','', data)
			data=re.sub(r'[\x3A-\x40]+','', data)
			data=" ".join(data.split())
			train.append((data, category))
				
	os.chdir('../..')

cl = NaiveBayesClassifier(train)

model_pkl = open('data.pkl', 'wb')
pickle.dump(cl, model_pkl)
model_pkl.close()

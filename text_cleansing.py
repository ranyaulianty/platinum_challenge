import pandas as pd
import re
from unidecode import unidecode
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory, StopWordRemover, ArrayDictionary
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import csv

#Turn all the letter to lower case
def lower_case(s):
    return s.lower()

#Wipe out punctuations
def remove_punctuation(s):
    s = re.sub(r"\\x[A-Za-z0-9./]+", '', unidecode(s))
    return re.sub(r"[^\w\d\s]+","",s)

#Wipe out new line
def remove_newline(s):
    return s.strip().replace(r'\n'," ")

#Wipe out multi-spaces
def remove_spaces(s):
    return  re.sub(' +', ' ',s)

#Wipe out links
def remove_link(s):
    s = re.sub(r'http\S+', '', s)
    s = re.sub(r"www.\S+", "", s)
    return s

#Wipe out hashtags
def remove_hashtag(s):
    s = re.sub("@[A-Za-z0-9_]+","", s)
    s = re.sub("#[A-Za-z0-9_]+","", s)
    return s

#Wipe out Indonesian stopwords -> sw stopwords
factory = StopWordRemoverFactory()
stopwords = factory.get_stop_words()
#nambahin stopword jika kurang
#memasukan data untuk proses normalisasi ke dalam variable bentuk array 1D
with open('D:\BINAR DATA SCIENCE\CHAPTER 9\TUGAS BESAR PLATINUM\platinum_\DATA\id_stopwords.csv', newline='') as csvfile:
    data_stopword_id = list(csv.reader(csvfile))

data_stopword_id
stopword_more = [item for sublist in data_stopword_id for item in sublist]
data_stopwords = stopwords + stopword_more
dictionary = ArrayDictionary(data_stopwords)
stopword = StopWordRemover(dictionary)

def stopwords_remove(content):
  text_add_space = re.sub(r" ","  ",str(content))
  tweet_remove = stopword.remove(text_add_space)
  text_remove_space = re.sub(r"  "," ",str(tweet_remove))
  tweet_clear = text_remove_space.strip()
  return tweet_clear

kamus = pd.read_csv('D:\BINAR DATA SCIENCE\CHAPTER 9\TUGAS BESAR PLATINUM\platinum_\DATA\kamusalay.csv', names = ['sebelum', 'sesudah'], encoding='latin-1')

number = 0

#Turns slang words to formal words
def _normalization(s):
  global number
  words = s.split()
  clear_words = ""
  for val in words:
    x = 0
    for idx, data in enumerate(kamus['sebelum']):
      if(val == data):
        clear_words += kamus['sesudah'][idx] + ' '
        print(number,"Transform :",data,"-",kamus['sesudah'][idx])
        x = 1
        number += 1
        break
    if(x == 0):
      clear_words += val + ' '
  return clear_words

def indo_stemming(s):
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    return stemmer.stem(s)
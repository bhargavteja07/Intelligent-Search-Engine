"""
Developer Name: Bhargav Arisetty
UIN: 679331171
UserID: marise2@uic.edu
"""

from nltk import PorterStemmer
import regex as reg
import yaml

stopwords_file_path = 'stopwords.txt'
doc_collection_path = 'www/abstracts/'
doc_collection_path_gold = 'www/gold/'
main_stop_words = []

def get_doc_collection_path():
    return doc_collection_path


def get_doc_collection_path_gold():
    return doc_collection_path_gold


def fetch_paths():
    global stopwords_file_path
    global doc_collection_path
    global doc_collection_path_gold
    with open("config.yml", 'r') as stream:
        paths_data = yaml.load(stream)
        stopwords_file_path = paths_data['stopwords_file_path']
        doc_collection_path = paths_data['doc_collection_path_abstract'] + '/'
        doc_collection_path_gold = paths_data['doc_collection_path_gold'] + '/'


def word_without_punctuations(word):
    refined_word = reg.sub('[^a-zA-Z]+', '', word)
    refined_word = refined_word.lower().strip()
    return refined_word


def refine_token(token):
    stemmer = PorterStemmer()
    refined_token = word_without_punctuations(token)

    #stopwords = get_stopwords()
    if refined_token in main_stop_words:
        return ''
    refined_token = stemmer.stem(refined_token)
    if refined_token not in main_stop_words and refined_token != '':
        return refined_token
    else:
        return ''


def get_valid_token_subset(word_list):
    subset_words = []
    valid_pos_tags = ['NN', 'NNS', 'NNP', 'NNPS', 'JJ']
    for word in word_list:
        pos_tag = word.split('_')[-1]
        if pos_tag in valid_pos_tags:
            subset_words.append(word)
    return subset_words


def tokenize_data_with_stemming_for_gold(doc_content):
    stemmer = PorterStemmer()
    word_list = []
    for phrase in doc_content.split('\n'):
        word_list.append(" ".join([stemmer.stem(word_without_punctuations(word)).lower().strip() for word in phrase.split()])) #viz list.join
    return word_list


def tokenize_data_with_stemming(doc_content):
    stemmer = PorterStemmer()
    word_list = [stemmer.stem(word_without_punctuations(word.split('_')[0])).strip() + '_' + word.split('_')[-1] for word in doc_content.split()]
    return word_list


def tokenize_data_for_valid_nodes(word_list):

    collection_tokens = []

    for word in word_list:
        word_formatted = refine_token(word)
        if word_formatted != '':
            collection_tokens.append(word_formatted)
    return collection_tokens


def get_content(doc_path):
    with open(doc_path) as doc_obj:
        doc_content = doc_obj.read()
        return doc_content


def tokenize_data_with_stemming_for_gold_v2(doc_content):
    stemmer = PorterStemmer()
    word_list = []
    stopwords = get_stopwords()
    for phrase in doc_content.split('\n'):
        s = []
        for word in phrase.split():
            if word not in stopwords:
                s.append(stemmer.stem(word_without_punctuations(word)).lower().strip())
        word_list.append(" ".join(s))#" ".join([stemmer.stem(word_without_punctuations(word)).lower().strip() for word in phrase.split()])) #viz list.join
    return word_list


def get_stopwords():
    global main_stop_words
    with open(stopwords_file_path) as sf:
        stopwords = sf.readlines()
        stopwords = [x.lower().strip() for x in stopwords]
    main_stop_words = stopwords

get_stopwords()
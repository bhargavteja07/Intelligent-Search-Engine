import utilities as ut
import math
from collections import defaultdict
import json


pre_computed_doc_lengths = {}
document_frequency = defaultdict(int)
index_file ={}
spider = {}


def get_spider():
    return spider


def get_idf(df):
    N = len(spider)
    return math.log2(N/df)


def construct_documnet_frequeny(document_frequency, valid_nodes):

    for node in list(set(valid_nodes)):
        document_frequency[node] += 1
    return document_frequency


def get_document_term_frequencies(valid_nodes):

    tf_dict = defaultdict(int)
    for node in valid_nodes:
        tf_dict[node.split('_')[0]] += 1
    return tf_dict


def compute_tf_idf_score(spider, document_frequency):

    for document_name in spider.keys():
        token_list = spider[document_name]['term_frequecy_vector'].keys()
        tf_dict_for_doc = spider[document_name]['term_frequecy_vector']
        tf_idf_dict_for_doc = defaultdict(int)
        for token in token_list:
            for word in token.split():
                tf_idf_dict_for_doc[token] += tf_dict_for_doc[word] * get_idf(document_frequency[word])

        spider[document_name]['tf_idf_vector'] = tf_idf_dict_for_doc
    return spider


def run_vectorizer():
    for doc in spider.keys():
        data = spider[doc]['text']
        tokens = ut.tokenize_data_for_valid_nodes(data.split())
        spider[doc]['vector'] = tokens
        construct_documnet_frequeny(document_frequency, tokens)
        term_frequency_dict = get_document_term_frequencies(tokens)
        spider[doc]['tf_idf_vector'] = term_frequency_dict
        update_index_file(term_frequency_dict, doc)

    pass


def update_index_file(word_formatted, doc_id):

    for word in word_formatted.keys():
        if word in index_file:
            index_file[word][doc_id] = word_formatted[word]
        else:
            index_file[word] = {doc_id:word_formatted[word]}


def get_tf_dict_for_query(ref_query_tokens):
    tf_dict_for_query = {}
    for token in ref_query_tokens:
        if token not in tf_dict_for_query:
            tf_dict_for_query[token] = 1
        else:
            tf_dict_for_query[token] += 1

    return tf_dict_for_query


def pre_compute_document_lengths():
    for doc_id in spider.keys():
        doc_length = 0
        doc_words_list = spider[doc_id]['tf_idf_vector']
        for word in doc_words_list:
            idf = get_idf(document_frequency[word])
            weight = index_file[word][doc_id] * idf
            weight = weight * weight
            doc_length += weight
        pre_computed_doc_lengths[doc_id] = doc_length


def get_query_length(tf_dict_for_query):
    query_length = 0
    for q_token, qtf in tf_dict_for_query.items():
        if q_token in index_file:
            weight = qtf * get_idf(document_frequency[q_token])
            weight = weight * weight
            query_length += weight
    query_length = math.sqrt(query_length)
    return query_length


def get_document_length(doc_id):
    return pre_computed_doc_lengths[doc_id]


def compute_cosine_sim(ref_query_tokens, doc_id):
    tf_dict_for_query = get_tf_dict_for_query(ref_query_tokens)
    numerator = 0
    for q_token, qtf in tf_dict_for_query.items():
        if q_token in index_file:
            if doc_id in index_file[q_token]:
                idf = get_idf(document_frequency[q_token])
                query_weight_for_word = qtf * idf
                doc_weight_for_word = index_file[q_token][doc_id] * idf
                numerator += query_weight_for_word * doc_weight_for_word

    query_length = get_query_length(tf_dict_for_query)
    doc_length = get_document_length(doc_id)

    doc_length = math.sqrt(doc_length)
    denominator = query_length * doc_length
    similarity = 0
    if denominator != 0:
        similarity = numerator/denominator
    return similarity


def main():
    global spider
    with open('Crawler/Spider.json') as f:
        spider = json.load(f)
        run_vectorizer()
        pre_compute_document_lengths()
        print("TF-IDF vector constructed")
    pass


main()

from collections import defaultdict
import json

graph = defaultdict(int)
page_rank_dict = {}
spider = {}


def get_page_rank_dict():
    return page_rank_dict


def web_graph():
    return graph


def harmonic_mean(tf_idf_score, page_rank_score):
    h_mean = (2 * tf_idf_score * page_rank_score)/(tf_idf_score + page_rank_score)
    return h_mean


def sort_docs_based_on_page_rank(docs_list):
    page_subset = {key:page_rank_dict[key] for key in docs_list}
    docs_sorted = sorted(page_subset, key=page_subset.get, reverse=True)
    return docs_sorted


def sort_docs_based_on_page_rank_v2(docs_list, docs_for_query):
    page_subset = {key:page_rank_dict[key] * docs_for_query[key] for key in docs_list}
    docs_sorted = sorted(page_subset, key=page_subset.get, reverse=True)
    return docs_sorted


def page_rank_graph():
    for node in spider.keys():
        graph[node] = defaultdict(int)
    for node in graph.keys():
        for out_node in spider[node]['out_links']:
            if out_node in graph and out_node != node:
                graph[node][out_node] += 1
                graph[out_node][node] += 1
        page_rank_dict[node] = 1/len(spider)


def compute_page_rank(word_graph):

    n = len(word_graph)
    param_alpha = 0.85
    param_pi = 1/n
    constant_factor = (1 - param_alpha) * param_pi
    for _ in range(10):
        for node in word_graph:
            s_vi = 0
            for adj_node_j in word_graph[node]:
                weight_jk = 0
                weight_ji = word_graph[adj_node_j][node]
                for adj_node_k in word_graph[adj_node_j]:
                    weight_jk += word_graph[adj_node_j][adj_node_k]
                if weight_jk != 0:
                    s_vj = page_rank_dict[adj_node_j]
                    s_vi += ((weight_ji/weight_jk) * s_vj) #+ constant_factor
            s_vi = (param_alpha * s_vi) + constant_factor
            page_rank_dict[node] = s_vi
    return page_rank_dict


def get_page_rank_sum(page_rank_scores, n_gram_list):
    sum = 0
    for word in n_gram_list:
        sum += page_rank_scores[word]
    return sum


def main():
    global spider
    with open('Crawler/Spider.json') as f:
        spider = json.load(f)
        page_rank_graph()
        compute_page_rank(graph)
    print("Web Graph constructed Using Page Ranking")


main()

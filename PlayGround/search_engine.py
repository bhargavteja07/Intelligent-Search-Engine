import page_rank_graph as pr
import vector_model as vm
import utilities as ut


def retrieve_docs_for_query(ref_query_tokens):
    spider = vm.get_spider()
    doc_weights = {}
    for doc in spider:
        doc_weights[doc] = vm.compute_cosine_sim(ref_query_tokens, doc)
    sorted_similarity = sorted(doc_weights, key=doc_weights.get, reverse=True)

    return sorted_similarity[:500]


def retrieve_docs_for_query_v2(ref_query_tokens):
    spider = vm.get_spider()
    doc_weights = {}
    for doc in spider:
        doc_weights[doc] = vm.compute_cosine_sim(ref_query_tokens, doc)
    return doc_weights


def execute_query_v2(query):
    query_tokens = query.split()
    refined_query_tokens = ut.tokenize_data_for_valid_nodes(query_tokens)
    docs_for_query = retrieve_docs_for_query_v2(refined_query_tokens)
    sorted_similarity = sorted(docs_for_query, key=docs_for_query.get, reverse=True)
    docs_based_on_page_rank = pr.sort_docs_based_on_page_rank_v2(sorted_similarity[:100], docs_for_query)
    print("docs based on tfidf - {0}".format(sorted_similarity[:20]))
    return docs_based_on_page_rank[:20]


def execute_query(query):
    query_tokens = query.split()
    refined_query_tokens = ut.tokenize_data_for_valid_nodes(query_tokens)
    spider = vm.get_spider()
    # c = 0
    # urls = []
    # for doc in spider:
    #     dts = spider[doc]['vector']
    #     if set(refined_query_tokens).intersection(set(dts)) == len(refined_query_tokens):
    #         c += 1
    #         urls.append(doc)
    #
    # print(urls)
    # print(c)

    docs_for_query = retrieve_docs_for_query(refined_query_tokens)
    docs_based_on_page_rank = []
    for i in range(10):
        docs_based_on_page_rank += pr.sort_docs_based_on_page_rank(docs_for_query[((i+1)*10 - 10):(i+1)*10])
    print("docs based on tfidf - {0}".format(docs_for_query[:20]))
    return docs_based_on_page_rank[:20]


def main():

     print(execute_query_v2("chicago evl"))
     print(execute_query_v2("computer science"))


#main()

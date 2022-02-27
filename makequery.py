import numpy as np
import math
from textprocessing import text_to_list, get_word_from_idx


def weight(N, tf, df):
    """
    using the tf, df terms, uses tf-idf weight function to return scalar value

    :param N: number of documents in the collection (usually 10)
    :param tf: term frequency in a given document
    :param df: database frequency of term in collection
    :return: float value
    """
    if tf == 0:
        return 0

    return (1 + math.log10(tf)) * math.log10(N / df)


def rocchio_algo(relevant_matrix, irrelevant_matrix, query_prev, alpha=1, beta=0.75, gamma=0.15):
    """

    :param relevant_matrix:
    :param irrelevant_matrix:
    :param query_prev:
    :param alpha:
    :param beta:
    :param gamma:
    :return:
    """
    num_relevant = len(relevant_matrix)
    num_irrelevant = len(irrelevant_matrix)

    relevant_vec = beta * np.sum(relevant_matrix, axis=0) / num_relevant
    irrelevant_vec = gamma * np.sum(irrelevant_matrix, axis=0) / num_irrelevant
    change = relevant_vec - irrelevant_vec
    query_next = (alpha * query_prev) + relevant_vec - irrelevant_vec

    return query_next / np.sum(query_next)


def get_query_words(prev_query, next_query, bag_of_words):
    """

    :param prev_query:
    :param next_query:
    :param bag_of_words: dictionary of words -- that map to --> dictionary with index and frequency of word
    example of a key: value in bag of words
        "cup": {"index": 1,
                "freq": 5}
    :return:
    """

    # TODO maybe we should rearrange the words
    # then we return the query --> we can also consider the query_next weights for the words we have already and rearrange the order
    a = 1.5
    # find the index for the words in prev_query and make it 0 in next_query
    for query_word in prev_query:
        next_query[bag_of_words[query_word]["index"]] = -1 * math.inf

    max_idxs = np.argpartition(next_query, -3)[-3:]  # indices in ascending value order
    sorted_max = next_query[max_idxs]

    new_query_words = list()
    new_query_words.append(get_word_from_idx(max_idxs[2], bag_of_words))
    if a * (sorted_max[2] - sorted_max[1]) <= (sorted_max[1] - sorted_max[0]):
        new_query_words.append(get_word_from_idx(max_idxs[1], bag_of_words))

    a = get_word_from_idx(max_idxs[0], bag_of_words)
    b = get_word_from_idx(max_idxs[1], bag_of_words)
    c = get_word_from_idx(max_idxs[2], bag_of_words)

    return new_query_words


def get_document_matrix(docs, bag_of_words, N):
    """

    :param docs:
    :param bag_of_words: dictionary of words -- that map to --> dictionary with index and frequency of word
    example of a key: value in bag of words
        "cup": {"index": 1,
                "freq": 5}
    :param N:
    :return:
    """
    m = np.zeros((len(docs), len(bag_of_words)))
    for k in range(len(docs)):
        doc = text_to_list(docs[k]["summary"])

        doc_tf = [0] * len(bag_of_words)  # document vector initialized to 0's

        # doc_tf has the frequency count of each term
        for term in doc:
            doc_tf[bag_of_words[term]["index"]] += 1

        # now find the if-idf weights for the document
        doc_vec = np.zeros((len(bag_of_words)))
        for word in bag_of_words.values():
            idx = word["index"]
            tf = doc_tf[idx]
            df = word["freq"]
            w = weight(N, tf, df)
            doc_vec[idx] = w
        m[k] = doc_vec

    return m

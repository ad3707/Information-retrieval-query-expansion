import pprint
import sys

from googleapi import *
from textprocessing import *
from makequery import *


def get_feedback_from_user(user_res):
    """
    iterates through search results returned from external API
    asks user if result is relevant

    :param user_res: list of json documents
    :return: tuple of list of json relevant documents, list of json irrelevant documents
    """
    relevant_docs = list()
    irrelevant_docs = list()

    print("\nGoogle Search Results:\n" + "=" * 30)
    for i in range(1, 1 + len(user_res)):
        print("RESULT " + str(i) + "\n" + "-" * 20)
        doc = user_res[i - 1]
        pprint.pprint(doc)
        feedback = input("Relevant? (Y/N)  ")
        while True:
            if feedback == "Y" or feedback == "N":
                break
            else:
                feedback = input("Enter valid response. Y or N only.")

        if feedback == "Y":
            relevant_docs.append(doc)
        else:
            irrelevant_docs.append(doc)

    return relevant_docs, irrelevant_docs


def is_precision_meet(target_value, relevant_docs, irrelevant_docs):
    """
    returns whether target precision established by the user is met with previous api search

    :param target_value: target precision that the user established
    :param relevant_docs: list of json relevant documents that contain summary, title, and url
    :param irrelevant_docs: list of json irrelevant documents that contain summary, title, and url
    :return: True or False boolean
    """
    num_documents = len(relevant_docs) + len(irrelevant_docs)
    precision = len(relevant_docs) / num_documents
    if target_value <= precision:
        return True, precision
    return False, precision


def main():
    args = tuple(sys.argv[1:])
    if not valid_args(args):
        print("Invalid arguments.")
        print("Usage: python3 retrieval.py <google api key> <google engine id> <precision> <query>")
        return

    key, engine_id, target_precision, raw_query = args
    print(type(raw_query))
    target_precision = float(target_precision)
    query_li = text_to_list(raw_query)
    docs, num_of_results = get_results(raw_query, target_precision, key, engine_id)

    if num_of_results < 10:
        print("Less than 10 results were found in first iteration.\nProgram will terminate.")  # TODO: later problem
        return

    relevant_docs, irrelevant_docs = get_feedback_from_user(docs)
    if len(relevant_docs) == 0:
        print("No relevant documents found in first iteration.\nProgram will terminate.")
        return

    precision_meet, current_precision = is_precision_meet(target_precision, relevant_docs, irrelevant_docs)
    while not precision_meet:
        bag_of_words = make_bag_of_words(query_li, docs)
        q_vec = vectorize_text(query_li, bag_of_words)

        N = len(relevant_docs) + len(irrelevant_docs)
        relevant_m = get_document_matrix(relevant_docs, bag_of_words, N)
        irrelevant_m = get_document_matrix(irrelevant_docs, bag_of_words, N)

        next_q_vec = rocchio_algo(relevant_m, irrelevant_m, np.array(q_vec))
        next_q_list = get_query_words(query_li, next_q_vec, bag_of_words)
        next_q = " ".join(query_li + next_q_list)

        print("\n\tFEEDBACK SUMMARY")
        print("New Query:", next_q)
        print("Current Precision:", current_precision)
        print("Still below the desired precision of", target_precision)
        print("\nIndexing results ...\n")
        print("Augmenting by", " ".join(next_q_list))

        user_res, num_of_results = get_results(next_q, target_precision, key, engine_id)
        relevant_docs, irrelevant_docs = get_feedback_from_user(user_res)

        precision_meet, current_precision = is_precision_meet(target_precision, relevant_docs, irrelevant_docs)
        query_li = query_li + next_q_list

    print("\n\nFINAL FEEDBACK SUMMARY")
    print("Query:", next_q)
    print("Precision Reached:", current_precision)

if __name__ == '__main__':
    main()

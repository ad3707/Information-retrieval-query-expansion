import pprint
from googleapiclient.discovery import build
import numpy as np
import random
import math

key = "AIzaSyAGmypTtalCS9lLgosvQiBQBIJ3FbviylU"  # TODO: make an environment variable
id = 'e1418010197679c8b'


# TODO: break apart files & add in comments

def get_results(query, target_precision):
    """
    TODO
    :param target_precision:
    :param query:
    :return:
    """
    service = build("customsearch", "v1",
                    developerKey=key)

    res = service.cse().list(
        q=query,
        cx=id,
    ).execute()

    print("Query:", query)
    print("Precision:", target_precision)

    user_res = list()
    num_of_results = len(list(res["items"]))

    for result in res["items"]:
        if "fileType" in result:
            print("PDF FOUND !!")
            continue

        document = {"title": result["title"],
                    "url": result["formattedUrl"],
                    "summary": result["snippet"]}
        user_res.append(document)

    return user_res, num_of_results


def get_feedback_from_user(user_res):
    """
    TODO
    """
    relevant_docs = list()
    irrelevant_docs = list()

    print("\nGoogle Search Results:\n" + "=" * 30)
    for i in range(1, 1+len(user_res)):
        print("RESULT " + str(i) + "\n" + "-" * 20)
        doc = user_res[i-1]
        pprint.pprint(doc)
        feedback = input("Relevant? (Y/N)  ")  # TODO: error checking stuff
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


def make_bag_of_words(query_li, relevant_docs, irrelevant_docs):
    """
    TODO
    :param query_li:
    :param relevant_docs:
    :param irrelevant_docs:
    :return:
    """
    bag_of_words = dict()
    idx = 0
    words = query_li.copy()
    for doc in irrelevant_docs + relevant_docs:
        words += text_to_list(doc["title"])
        words += text_to_list(doc["summary"])
    for word in words:
        if word in bag_of_words:
            bag_of_words[word]["freq"] += 1
        else:
            bag_of_words[word] = {"index": idx,
                                  "freq": 1}
            idx += 1
    return bag_of_words


def clean_word(word):
    # TODO
    return word.lower()
    # return ''.join(ch for ch in word if
    #               ch.isalnum()).lower()


def text_to_list(text):
    return [clean_word(w) for w in text.split()]


def is_precision_meet(target_value, relevant_docs, irrelevant_docs):
    num_documents = len(relevant_docs) + len(irrelevant_docs)
    precision = len(relevant_docs) / num_documents
    if target_value <= precision:
        return True, precision
    return False, precision


def rocchio_algo(relevant_docs, irrelevant_docs, query_prev, alpha=1, beta=0.75, gamma=0.15):
    num_relevant = len(relevant_docs)
    num_irrelevant = len(irrelevant_docs)

    query_next = (alpha * query_prev) + (beta * (np.sum(relevant_docs))/num_relevant) - gamma * (np.sum(irrelevant_docs))/num_irrelevant
    return query_next




def vectorize_text(list_of_words, bag_of_words):
    """
    :param bag_of_words:
    :param list_of_words:
    :param text:
    :return:
    """
    vec = [0] * len(bag_of_words)
    for term in list_of_words:
        vec[bag_of_words[term]["index"]] += 1

    return vec / np.sum(vec)


def get_query_words(prev_query, next_query, bag_of_words):
    """
    TODO maybe we should rearrange the words
        # then we return the query --> we can also consider the query_next weights for the words we have already and rearrange the order

    :param prev_query:
    :param next_query:
    :param bag_of_words:
    :return:
    """
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


def get_word_from_idx(idx, bag_of_words):
    for word, value in bag_of_words.items():
        if value["index"] == idx:
            return word
    return ""


def weight(N, tf, df):
    if tf == 0:
        return 0

    return (1 + math.log10(tf)) * math.log10(N / df)


def get_document_matrix(docs, bag_of_words, N):
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


def main():
    raw_query = input("Search: ")
    target_precision = float(input("Precision: ")) # TODO: ERROR CHECKING
    query_li = text_to_list(raw_query)
    user_res, num_of_results = get_results(raw_query, target_precision)


    if num_of_results < 10:
        print("Less than 10 results were found in first iteration.\nProgram will terminate.")  # TODO: later problem
        return

    relevant_docs, irrelevant_docs = get_feedback_from_user(user_res)
    if len(relevant_docs) == 0:
        print("No relevant documents found in first iteration.\nProgram will terminate.")
        return  # TODO: later problem

    precision_meet, current_precision = is_precision_meet(target_precision, relevant_docs, irrelevant_docs)
    while not precision_meet:
        bag_of_words = make_bag_of_words(query_li, relevant_docs, irrelevant_docs)
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


        user_res, num_of_results = get_results(next_q, target_precision)
        relevant_docs, irrelevant_docs = get_feedback_from_user(user_res)

        precision_meet, current_precision = is_precision_meet(target_precision, relevant_docs, irrelevant_docs)
        query_li = query_li + next_q_list

    print("Done.")

if __name__ == '__main__':
    print(main())

import numpy as np


def make_bag_of_words(query_li, docs):
    """
    creates a bag of words representation using all of the titles + summaries of the documents as well as the current query
    creates a dictionary where each unique words has an assigned index and frequency of the word in the collection

    :param query_li: list of query words
    :param relevant_docs: list of json relevant documents that contain summary, title, and url
    :param irrelevant_docs: list of json irrelevant documents that contain summary, title, and url
    :return: dictionary of words -- that map to --> dictionary with index and frequency of word
    
    example of a key: value in bag of words
        "cup": {"index": 1,
                "freq": 5}
    """
    bag_of_words = dict()
    idx = 0
    words = query_li.copy()

    for word in words:
        if word in bag_of_words:
            bag_of_words[word]["freq"] += 1
        else:
            bag_of_words[word] = {"index": idx,
                                  "freq": 1,
                                  "df-freq": 0,
                                  "docs": set()}
            idx += 1

    for i in range(len(docs)):
        doc = docs[i]
        words = text_to_list(doc["title"]) + text_to_list(doc["title"])
        words += text_to_list(doc["summary"])
        for word in words:
            if word in bag_of_words:
                bag_of_words[word]["freq"] += 1
                bag_of_words[word]["docs"].add(i)
                bag_of_words[word]["df-freq"] = len(bag_of_words[word]["docs"])
            else:

                bag_of_words[word] = {"index": idx,
                                      "freq": 1,
                                      "df-freq": 1,
                                      "docs": {i}}
                idx += 1
    return bag_of_words


def clean_word(word):
    """
    preprocesses the string by turning it into lower-case

    :param word: string
    :return: lower-case string
    """
    return ''.join(ch for ch in word if ch.isalnum()).lower()
    return word.lower() #TODO


def text_to_list(text):
    """
    takes a string and splits it into a list by " "

    :param text: string that contains words
    :return: list of string words
    """
    return [clean_word(w) for w in text.split()]


def vectorize_text(list_of_words, bag_of_words):
    """
    creates a vector of length N where N is the number of words in the bag of words representation
    iterates through every word in list and generates the frequency of the words
    normalizes the vector

    :param bag_of_words: dictionary of words -- that map to --> dictionary with index and frequency of word
    example of a key: value in bag of words
        "cup": {"index": 1,
                "freq": 5}
    :param list_of_words: list of strings that was created by text_by_list
    :return: a list of N integers where N is the number of words in the bag of words representation
    """
    vec = [0] * len(bag_of_words)
    for term in list_of_words:
        vec[bag_of_words[term]["index"]] += 1

    return vec / np.sum(vec)


def get_word_from_idx(idx, bag_of_words):
    """
    returns the word associated with a given index in the bag of words dictionary

    :param idx: index of word
dictionary of words -- that map to --> dictionary with index and frequency of word
    example of a key: value in bag of words
        "cup": {"index": 1,
                "freq": 5}
    :return: word that corresponds to index or empty string
    """
    for word, value in bag_of_words.items():
        if value["index"] == idx:
            return word
    return ""

**Name & Uni:**
        Aditi Dam ad3707
        Shivani Patel svp2128

**List of Files:**
retrieval.py 
README.md

**How to Run:**

        ** write down all commands for software and dependencies **

**Internal Design Description:**

get_results: 
This function returns the top 10 google results to the user. It also checks that they are all html files. 

get_feedback_from_user: 
This function prints out the google search results one by one and asks the user if it is relevant for their search. It creates two lists of relevant and irrelevant docs and appends documents to one of the list based on the user feedback. It also does error checking to ensure the user only enters in Y or N for yes and no. 

make_bag_of_words:
This function creates a bag of words which is a multiset of the words found in the documents. It assigns an index and a frequency of each word. If the word is already found in the bag of words representation, then it would increment the frequency by 1.

clean_word:
This function preprocesses the word passed in by turning it into lowercase. 

text_to_list: 
This function splits the the text into a list using the split method. 

is_precision_meet:
This function checks if the target precision is met. It calculates precision by taking the relevant documents and dividing it by the total number of documents. It returns the current precision value and a a boolean value of whether the target precision is met or not. 

roccio_algo:
This function implements Rocchio's algorithm which is used to determine the query term weights in the next query. We set alpha to 1, beta to 0.75, and gamma to 0.15 based on this article https://nlp.stanford.edu/IR-book/html/htmledition/the-rocchio71-algorithm-1.html. 

vectorize_text:
This function initializes a vector and normalizes it. 

get_query_words:
This function returns the words we are augmenting to the new query. If the word is already in the query, we set it to negative infinity. The algorithm for this function is that it gives the indices of the top three weights in the matrix. If the product of a and the difference between the top two values are less than the third and second highest weights, then it will append the second highest and highest weighted word. Otherwise, it will just append the highest weighted word in the new query. 

get_word_from_idx:
This function returns the word associated with the given index in the bag of words representation. 

weight:
This function assigns the tf-idf weights to the terms. 

get_document_matrix:
This function initializes the document vector and finds the tf and df for the documents. 

main: 
The main function prompts the user to enter their search query and target precision. It checks that the number of results is greater or equal to 10. It also checks that in the first iteration there are relevant documents. While the precision is not met, it calls all the previous functions and prints a summary of each iteration. 

External libraries: pprint- pretty print to customize the formatting of the output, numpy - for manipulating matrices, math, googleapiclient.discovery 

**Query-modification Method fo Description: **


**Google Custom Search Engine JSON API Key:**
key = "AIzaSyAGmypTtalCS9lLgosvQiBQBIJ3FbviylU"

**Engine ID:**
id = 'e1418010197679c8b'


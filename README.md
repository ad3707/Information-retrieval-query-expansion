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

get_feedback_from_user: 
This function prints out the google search results one by one and asks the user if it is relevant for their search. It creates two lists of relevant and irrelevant docs and appends documents to one of the list based on the user feedback. It also does error checking to ensure the user only enters in Y or N for yes and no. 

make_bag_of_words:

clean_word:
This function preprocesses the word passed in by turning it into lowercase. 

text_to_list:

is_precision_meet:
This function checks if the target precision is met. It calculates precision by taking the relevant documents and dividing it by the total number of documents. It returns the current precision value and a a boolean value of whether the target precision is met or not. 

roccio_algo:
This function implements Rocchio's algorithm which is used to determine the query term weights in the next query. We set alpha to 1, beta to 0.75, and gamma to 0.15 based on this article https://nlp.stanford.edu/IR-book/html/htmledition/the-rocchio71-algorithm-1.html. 

vectorize_text:

get_query_words:

get_word_from_inx:

weight:

get_document_matrix:

main: 



**Query-modification Method fo Description: **


**Google Custom Search Engine JSON API Key:**
key = "AIzaSyAGmypTtalCS9lLgosvQiBQBIJ3FbviylU"

**Engine ID:**
id = 'e1418010197679c8b'


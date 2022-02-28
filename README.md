##Name & Uni:
        Aditi Dam ad3707  
        Shivani Patel svp2128

## List of Files:
*retrieval.py*  
textprocessing.py  
googleapi.py  
textprocessing.py  
requirements.txt
README.md

# How to Run:

        sudo apt-get update
        sudo apt-get install python3-pip
        sudo apt-get install python3-venv
        python3 -m venv dbproj
        pip install -r requirements.txt
        python3 retrieval.py "AIzaSyAGmypTtalCS9lLgosvQiBQBIJ3FbviylU" "e1418010197679c8b" <precision> <query word>

###Internal Design Description:

**retrieval.py:** main starter code that prompts the user for feedback and checks if the precision is met to stop the iterations  
  
  - get_feedback_from_user: promotes for user feedback to determine relevant and irrelevant documents  
  - is_precision_meet:  determines whether the target precision was reached
  - main:  validates command line arguments, performs search iterations until target precision is reached (or 0.0)

**makequery.py:** functions that relate to creating the next query. It contains the Rocchio algorithm to help determining the weights for the next iteration given relevancy
     
 - get_document_matrix: returns a matrix of document vectors where each entry in the vector corresponds to a term's weight  
 - rocchio_algo:  q_prev + 0.75 * sum of relevant weights + 0.15 * sum of irrelevant weights  
 - get_query_words:  finds top 3 words with the highest score in query vector and returns 1 or 2 determining on the scores  
    - if the difference between the top 2 words is greater by some factor > 1 than the difference between the 2nd and 3rd top word, then return 2 words
    - this adds 1 or 2 words depending on how spread out the scores of the words are
 - weight: using the term frequency in a particular document, and the document frequency, return the weight = (1 + log(tf)) * log(N/df)

**textprocess.py:** Creates the bag of words representation model and preprocessing for text

  - make_bag_of_words: processes a nested dictionary of words across documents and query  
    - each word contains a unique index, total frequency in databases, document frequency, and a set of docs that the word is in
    - each document's summary and the title * 2 is used as a representation of the document  
      - this puts an emphasis on the words in the title
  - clean_word: processes word to remove any non-alphanumeric values
  - text_to_list: produces a list of cleaned words
  - vectorize_text: converts a list of cleaned words into a vector representation that follows the BoW indices
  - get_word_from_idx: finds the corresponding word according to its BoW index

**googleapi.py:**
Contains functionality to retrieve top 10 google results from the API  
  - get_results: retrieves the top 10 results for a query and returns a list of dictionaries that contain the title, url, and summary
  - try_connection: tries to make a call to the api with the key and id
  - valid_args: verifies whether the connection to the api is valid  
####*non-HTML files were ignored.*

### External libraries:
- pprint - to pretty print any dictionary such as the document in get_user_feedback
- numpy - for document vectorization, to perform matrix operations such as element-wise addition; primarilly in makequery.py
- math - to find log of float values for weight in makequery.py
- sys - to retrieve command line arguments
- googleapiclient.discovery - connection to google api for searching

### Query-modification Method Description:

A bag of words representation was created which is a multiset of the words found in the documents. Each particular document summary, title, and title (twice) was used as the stream of text. This brings emphasis to the words that belong in the title of a document.  
Each words gets assigned a unique index as well and calculates the total frequency, document frequency, and the set of document indices that contain that word.
An entry in the bag of words may be like:  
    "potato": {  
                "index": 1,  
                "freq": 10,  
                "df-freq": 3,  
                "docs": {1,2,8}  
              }  

This is an iterative procedure across all documents with its representative words (summary + 2 * title)

To get the next query words, we must first update the previous query vector representation.
For each word already in query, we set its index to negative infinity. This would ensure that we will never pick the same word twice.

Using Rocchio's algorithm, the next query vector is determined from the previous query vector, relevant information matrix, and irrelevant information matrix.
The relevant and irrelevant information is represented as a matrix of N x M, where N is the number of documents and M is the number of words in the bag of words.
For each index in each row of the matrix, it corresponds to the weight of index. The weight is determined by the tf-idf weights where it uses each term frequency in a document and the document frequency of each word.
Then, we can sum across the documents for each term, and by adding the relevant weights and subtracting the irrelevant weights, we can find the next query.
We also normalized the query weights and set alpha to 1, beta to 0.75, and gamma to 0.15 based on this article https://nlp.stanford.edu/IR-book/html/htmledition/the-rocchio71-algorithm-1.html.

Then the top three scores in next query vector are found and the indices are recorded.
If the product of some scalar value > 1 and the difference between the top two values are less than the third and second highest weights, then it will append the highest and second highest weighted word in that order.
Otherwise, it will just append the highest weighted word in the new query. 

*We did not change the order of the query. We simply appended new query words found at the end of the query.*

Using the bag of words, we can find the word that corresponds to the index or indices that we want to add to the query.


### Parameters 

**Google Custom Search Engine JSON API Key:**
key = "AIzaSyAGmypTtalCS9lLgosvQiBQBIJ3FbviylU"

**Engine ID:**
id = 'e1418010197679c8b'



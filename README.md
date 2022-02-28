**Name & Uni:**
        Aditi Dam ad3707
        Shivani Patel svp2128

**List of Files:**
retrieval.py 
README.md

**How to Run:**

        ** write down all commands for software and dependencies **
        sudo apt-get update
        sudo apt-get install python3-pip
        sudo apt-get install python3-venv
        python3 -m venv dbproj
        pip install --upgrade google-api-python-client
        python3 retrieval.py "AIzaSyAGmypTtalCS9lLgosvQiBQBIJ3FbviylU" "e1418010197679c8b" <precision> <query word>

**Internal Design Description:**

We divided our code into separate files:

makequery.py: This file contains funcions that relate to creating the next query. It contains the Rocchio algorithm and the function for retrieivng the words associated with the highest weights. 

retrieval.py: This file contains the code that prompts the user for feedback and checks if the precision is met to stop the iterations. 

textprocess.py: This file deals with creating the bag of words representation model and preprocessing the text. 

googleapi.py: This file displays the top 10 google results from the API. 

External libraries: pprint- pretty print to customize the formatting of the output, numpy - for manipulating matrices, math, googleapiclient.discovery 

**Query-modification Method Description: **

A bag of words representation was created which is a multiset of the words found in the documents. It assigns an index and a frequency of each word. If the word is already found in the bag of words representation, then it would increment the frequency by 1. Bag of words also includes the title words twice to give them more weight. 

weight: This function assigns the tf-idf weights to the terms. 

We implemented Rocchio's algorithm which is used to determine the query term weights in the next query. We also normalized the weights and set alpha to 1, beta to 0.75, and gamma to 0.15 based on this article https://nlp.stanford.edu/IR-book/html/htmledition/the-rocchio71-algorithm-1.html. 

After we calculated the weights of the terms, the get_query_words function returns the words we are augmenting to the new query. If the word is already in the query, we set it to negative infinity. The algorithm for this function is that it gives the indices of the top three weights in the matrix. If the product of a and the difference between the top two values are less than the third and second highest weights, then it will append the highest and second highest weighted word in that order. Otherwise, it will just append the highest weighted word in the new query. 

After, we had a function called get_word_from_idx which returns the word associated with the given index in the bag of words representation. 

**Google Custom Search Engine JSON API Key:**
key = "AIzaSyAGmypTtalCS9lLgosvQiBQBIJ3FbviylU"

**Engine ID:**
id = 'e1418010197679c8b'


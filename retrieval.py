import pprint
from googleapiclient.discovery import build

key = "AIzaSyAGmypTtalCS9lLgosvQiBQBIJ3FbviylU"  # TODO: make an environment variable
id = 'e1418010197679c8b'


def get_results(query):
    """
    TODO
    :param query:
    :return:
    """
    service = build("customsearch", "v1",
                    developerKey=key)

    res = service.cse().list(
        q=query,
        cx=id,
    ).execute()

    user_res = list()
    pprint.pprint(res)
    for result in res["items"]:
        if "fileType" in result:
            print("PDF FOUND !!")
            continue

        document = {"title": result["title"],
                    "url": result["formattedUrl"],
                    "summary": result["snippet"]}
        user_res.append(document)

    return user_res

def get_feedback_from_user(user_res):
    """
    TODO
    """
    relevant_docs = list()
    irrelevant_docs = list()

    for doc in user_res:
        print("RESULT 1 \n" + "="*20)
        pprint.pprint(doc)
        feedback = input("Relevant? (Y/N)  ") # TODO: error checking stuff
        if feedback == "Y":
            relevant_docs.append(doc)
        elif feedback == "N":
            irrelevant_docs.append(doc)
        else:
            print("BRUH")
            return

    return relevant_docs, irrelevant_docs

def main():
    raw_query = "milky way"
    query = raw_query.lower()
    user_res = get_results(query)
    relevant_docs, irrelevant_docs = get_feedback_from_user(user_res)


if __name__ == '__main__':
    main()

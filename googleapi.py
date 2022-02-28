from googleapiclient.discovery import build


def valid_args(args):
    """
    returns whether args are valid and can process a call to the search engine
    checks for:
        (1) number of command line args
        (2) target precision is a float between 0 and 1
        (3) can successfully query first result using key and engine_id provided

    :param args: command line args as a tuple of strings
    :return: boolean True or False on whether the args given are valid or not
    """
    if len(args) != 4:
        return False
    key, engine_id, target_precision, raw_query = args

    try:
        if float(target_precision) > 1 or float(target_precision) < 0:
            return False
        r = try_connection(raw_query, key, engine_id)
        return True
    except:
        return False


def try_connection(query, key, engine_id):
    """
    function created to test connection using key and engine ID for Google Search API

    :param query: string that contains 1 or more words
    :param key: Google Custom Search Engine JSON API Key
    :param engine_id: Engine ID
    :return: result of query
    """
    service = build("customsearch", "v1",
                    developerKey=key)
    return service.cse().list(
        q=query,
        cx=engine_id,
    ).execute()


def get_results(query, target_precision, key, engine_id):
    """
    makes a call to the Google search engine api to find top 10 results for given query
    if non-html file, file is not returned in user_res[0]

    :param key: Google Custom Search Engine JSON API Key
    :param engine_id: Engine ID
    :param target_precision: float value between 0 and 1
    :param query: string that contains 1 or more words
    :return: tuple of results as a list of documents where which document is a dictionary with title, url, and summary and number of results
    """
    service = build("customsearch", "v1",
                    developerKey=key)

    res = service.cse().list(
        q=query,
        cx=engine_id,
    ).execute()

    print("Query:", query)
    print("Precision:", target_precision)

    if "items" not in res:
        return None, 0

    num_of_results = len(list(res["items"]))

    user_res = list()
    for result in res["items"]:
        if "fileType" in result:
            continue

        document = {"title": result["title"],
                    "url": result["formattedUrl"],
                    "summary": result["snippet"]}
        user_res.append(document)

    return user_res, num_of_results

import pprint
from googleapiclient.discovery import build


def main():
  service = build("customsearch", "v1",
            developerKey="AIzaSyAGmypTtalCS9lLgosvQiBQBIJ3FbviylU")

  res = service.cse().list(
      q='lectures',
      cx='017576662512468239146:omuauf_lfve',
    ).execute()
  pprint.pprint(res)

if __name__ == '__main__':
  main()

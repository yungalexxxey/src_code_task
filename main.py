"""Webservice for ОТКРЫТЫЙ КОД test task"""
import uvicorn

from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI

es = AsyncElasticsearch("http://localhost:9200")
app = FastAPI()


class SearchMatch:
    """Object, which contains all info about match in a convenient way"""

    def __new__(cls, es_raw_data: dict):
        if es_raw_data['hits']["hits"]:
            return super(SearchMatch, cls).__new__(cls)
        return None

    def __init__(self, es_raw_data: dict):
        self.index = es_raw_data['hits']['hits'][0]['_index']
        self.score = float(es_raw_data['hits']['hits'][0]['_score'])
        self.title = es_raw_data['hits']['hits'][0]['_source']['title']
        self.body = es_raw_data['hits']['hits'][0]['_source']['body']

    def parse_match(self):
        """returns json, based on object data"""
        return {
            'title': self.title,
            'body': self.body
        }

    def __repr__(self):
        return f"{self.index} - {self.title} - {self.body} - {self.score}"


async def get_matches(request: str):
    """Returns sorted list of all matches in elasticsearch"""
    all_indexes: dict = await es.indices.get_alias()
    list_of_matches = []
    for index in all_indexes.keys():
        es_response = await es.search(index=index, size=1, query={"match": {"body": request}})
        match_obj = SearchMatch(es_response)
        if match_obj:
            list_of_matches.append(match_obj)
    return sorted(list_of_matches, key=lambda x: x.score, reverse=True)


@app.get('/search')
async def search(request: str):
    """GET method returns JSON of founded documents in elasticsearch"""

    result = {}
    for match in await get_matches(request):
        result[match.index] = match.parse_match()
    return result


if __name__ == '__main__':
    uvicorn.run(app=app, host='localhost', port=1337)

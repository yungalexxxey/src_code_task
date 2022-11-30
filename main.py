"""Webservice for ОТКРЫТЫЙ КОД test task"""
import uvicorn

from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fuzzywuzzy import process

es = AsyncElasticsearch("http://localhost:9200")
app = FastAPI()

index_themes = {
    'новости': ["деревья на Садовом кольце", "добрый автобус", "выставка IT-технологий"],
    "кухня": ["рецепт борща", "яблочный пирог", "тайская кухня"],
    'товары': ["Дети капитана Гранта", "зимние шины", "Тайская кухня"]
}


def find_possible_indexes(request: str) -> list:
    """Finds all possible indexes"""
    possible_indexes = []
    for theme, value in index_themes.items():
        for match in process.extract(request, value):
            if match[1] > 65:
                possible_indexes.append(theme)
    return possible_indexes


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

    def parse_match(self) -> dict:
        """returns json, based on object data"""
        return {
            'title': self.title,
            'body': self.body
        }

    def __repr__(self):
        return f"{self.index} - {self.title} - {self.body} - {self.score}"


async def get_matches(request: str) -> list:
    """Returns sorted list of all matches in elasticsearch"""
    list_of_matches = []
    for index in find_possible_indexes(request):
        es_response = await es.search(index=index, size=1, query={"match": {"body": request}})
        match_obj = SearchMatch(es_response)
        if match_obj:
            list_of_matches.append(match_obj)
    return sorted(list_of_matches, key=lambda x: x.score, reverse=True)


@app.on_event('shutdown')
async def shutdown():
    """elasticsearch connection will be closed"""
    await es.close()


@app.get('/search')
async def search(request: str):
    """GET method returns JSON of founded documents in elasticsearch"""

    result = {}
    for match in await get_matches(request):
        result[match.index] = match.parse_match()
    return result


if __name__ == '__main__':
    uvicorn.run(app=app, host='localhost', port=1337)

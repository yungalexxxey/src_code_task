import asyncio
from elasticsearch import AsyncElasticsearch

es = AsyncElasticsearch("http://localhost:9200")

async def init_es():
    es_data = await es.search(query={"match_all": {}})
    if es_data['hits']['hits']:
        await es.close()
        print("Es was already initialized")
        return
    await es.index(
        index='новости',
        document={
            'title': 'деревья на Садовом кольце',
            'body': 'деревья на Садовом кольце'
        }
    )
    await es.index(
        index='новости',
        document={
            'title': 'добрый автобус',
            'body': 'добрый автобус'
        }
    )
    await es.index(
        index='новости',
        document={
            'title': 'выставка IT-технологий',
            'body': 'выставка IT-технологий'
        }
    )
    await es.index(
        index='кухня',
        document={
            'title': 'рецепт борща',
            'body': 'рецепт борща'
        }
    )
    await es.index(
        index='кухня',
        document={
            'title': 'яблочный пирог',
            'body': 'яблочный пирог'
        }
    )
    await es.index(
        index='кухня',
        document={
            'title': 'тайская кухня',
            'body': 'тайская кухня'
        }
    )
    await es.index(
        index='товары',
        document={
            'title': 'зимние шины',
            'body': 'зимние шины'
        }
    )
    await es.index(
        index='товары',
        document={
            'title': 'Дети капитана Гранта',
            'body': 'Дети капитана Гранта'
        }
    )
    await es.index(
        index='товары',
        document={
            'title': 'Тайская кухня',
            'body': 'Тайская кухня'
        }
    )
    await es.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(init_es())

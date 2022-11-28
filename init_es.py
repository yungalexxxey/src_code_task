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
            'body': 'Какая-то большая новость про деревья на Садовом кольце'
        }
    )
    await es.index(
        index='новости',
        document={
            'title': 'добрый автобус',
            'body': 'Какая-то небольшая новость про добрый автобус'
        }
    )
    await es.index(
        index='новости',
        document={
            'title': 'выставка IT-технологий',
            'body': 'Какая-то маленькая новость про выставка IT-технологий'
        }
    )
    await es.index(
        index='кухня',
        document={
            'title': 'рецепт борща',
            'body': 'Статья про то, что представляет из себя рецепт борща'
        }
    )
    await es.index(
        index='кухня',
        document={
            'title': 'яблочный пирог',
            'body': 'Статья про то, что представляет из себя яблочный пирог'
        }
    )
    await es.index(
        index='кухня',
        document={
            'title': 'тайская кухня',
            'body': 'Статья про то, что представляет из себя тайская кухня'
        }
    )
    await es.index(
        index='товары',
        document={
            'title': 'зимние шины',
            'body': 'Страничка, на которой рассказывается, зачем нужны зимние шины'
        }
    )
    await es.index(
        index='товары',
        document={
            'title': 'Дети капитана Гранта',
            'body': 'Страница о том, почему книга Дети капитана Гранта лучше фильма'
        }
    )
    await es.index(
        index='товары',
        document={
            'title': 'Тайская кухня',
            'body': 'Где купить Тайская кухня'
        }
    )
    await es.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(init_es())

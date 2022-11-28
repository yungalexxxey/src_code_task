# src_code_task

<h1> HOW TO INSTALL && RUN </h1>
run the commands sequentially:

1. sudo docker compose up -d
2. python3 -m venv venv
3. source ./venv/bin/activate
4. pip install -r requirements.txt
5. python3 init_es.py
6. python3 main.py

<h2> HOW TO RUN TESTS</h2>
After running web-service, you can run "pytest test.py" in another terminal to run autotests.


<h3> QUERY EXAMPLES</h3>

1. Query, which doesn't return any indexes: 
```
curl -X 'GET' \
  -G 'http://localhost:1337/search' \
  -H 'accept: application/json; charset= utf-8' \
--data-urlencode "request=123"
```
2. Query, which return result with only 1 index:
```
curl -X 'GET' \
  -G 'http://localhost:1337/search' \
  -H 'accept: application/json; charset= utf-8' \
--data-urlencode "request=шины"
```
3. Query, which return result with couple indexes:
```
curl -X 'GET' \
  -G 'http://localhost:1337/search' \
  -H 'accept: application/json; charset= utf-8' \
--data-urlencode "request=шины" 
```

EXAMPLE OF RESPONSE:

```
{
  "новости": {
    "title": "добрый автобус",
    "body": "Какая-то небольшая новость про добрый автобус"
  }
}
```

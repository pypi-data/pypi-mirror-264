# esqt - Elasticsearch Query Tool

[![pypi](https://img.shields.io/pypi/v/esqt.svg)](https://pypi.python.org/pypi/esqt)

## CLI

```sh
pipx install esqt
```

---

## `s` - scan (search) / source

```sh
cat <<EOF | esqt s localhost -vSd - | jq -c
{
  "query": {
    "bool": {
      "filter": [
        {
          "terms": {
            "itemTimestamp": [
              1707006570
            ]
          }
        }
      ]
    }
  }
}

EOF
```

## `q` - perform_request (request path)

```sh
esqt q localhost -X GET -P _cat/indices -p 'pretty=&format=json&v&s=index' | jq
```

## `t` - streaming_bulk (bulk) / target

```sh
esqt s localhost -vSd __.conf.json | esqt t localhost -d - | jq -c
```

```py
# dev.py
def my_handler(actions: t.Iterable[str]):
    for action in actions:
        yield json.loads(action)
```

```sh
esqt s localhost -vSd __.conf.json | esqt t localhost -d - -H dev:my_handler | jq -c
```

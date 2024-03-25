# esqt - Elasticsearch Query Tool

[![pypi](https://img.shields.io/pypi/v/esqt.svg)](https://pypi.python.org/pypi/esqt)

## CLI

```sh
pipx run esqt COMMAND
```

---

## `s` - scan (search)

```sh
cat <<EOF | pdm run esqt s localhost -vSd - | jq -c
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
pdm run esqt q localhost -X GET -P _cat/indices -p 'pretty=&format=json&v&s=index' | jq
```

## `t` - streaming_bulk (bulk)

```sh
pdm run esqt s localhost -vSd __.conf.json | pdm run esqt t localhost -H dev:DevHandler -d - | jq -c
```

from functools import reduce
import json
import typing as t


def parse_header(h: str) -> dict[str, str]:
    if h is None:
        return {}
    return dict([h.split(':', 1)])


def parse_params(s: str) -> dict[str, str]:
    if s is None:
        return {}
    result = {}
    for pair in s.split('&'):
        if '=' in pair:
            k, v = pair.split('=', 1)
        else:
            k, v = pair, ''
        result[k] = v
    return result


def merge_dicts(dicts: t.Optional[t.Iterable[dict[str, str]]]):
    return reduce(lambda acc, x: {**acc, **x}, dicts or [], t.cast(dict[str, str], {}))


def jobj_to_line(jobj):
    result = json.dumps(jobj, ensure_ascii=False)
    if not result.endswith('\n'):
        return result + '\n'
    return result

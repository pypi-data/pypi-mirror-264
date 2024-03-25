from contextlib import nullcontext
from contextlib import redirect_stdout
import json
from pathlib import Path
import sys
import time
import typing as t

from elasticsearch.helpers import scan
from elasticsearch.helpers import streaming_bulk
import typer
from uvicorn.importer import import_from_string

from . import es
from .utils import json_obj_to_line
from .utils import merge_dicts
from .utils import parse_header
from .utils import parse_params


app = typer.Typer()


@app.command(name='e')
def search(
    host: t.Annotated[str, typer.Argument(help='Elasticsearch host')] = 'localhost',
):
    client = es.Client(host=host)
    client.search


@app.command(name='s')
def scan_(
    host: t.Annotated[str, typer.Argument(help='Elasticsearch host')] = 'localhost',
    #
    scroll: t.Annotated[str, typer.Option('--scroll', help='Scroll duration')] = '5m',
    raise_on_error: t.Annotated[bool, typer.Option(' /--no-raise-on-error')] = True,
    preserve_order: t.Annotated[bool, typer.Option('--preserve-order')] = False,
    size: t.Annotated[int, typer.Option('--size')] = 1000,
    request_timeout: t.Annotated[t.Optional[int], typer.Option('--request-timeout')] = None,
    clear_scroll: t.Annotated[bool, typer.Option(' /--keep-scroll')] = True,
    #
    index: t.Annotated[
        t.Optional[str],
        typer.Option('-i', '--index', help='A comma-separated list of index names to search'),
    ] = None,
    #
    file_input_search_body: t.Annotated[
        t.Optional[typer.FileText], typer.Option('-d', '--data')
    ] = None,
    file_output: t.Annotated[typer.FileTextWrite, typer.Option('-o', '--output')] = t.cast(
        typer.FileTextWrite, sys.stdout
    ),
    #
    verbose: t.Annotated[bool, typer.Option('-v', '--verbose')] = False,
):
    search_body = file_input_search_body and file_input_search_body.read().strip() or '{}'
    client = es.Client(host=host)
    iterable = scan(
        client=client,
        query=search_body and json.loads(search_body),
        scroll=scroll,
        raise_on_error=raise_on_error,
        preserve_order=preserve_order,
        size=size,
        request_timeout=request_timeout,
        clear_scroll=clear_scroll,
        index=index,
    )
    progressbar = nullcontext(iterable)
    if verbose:
        progressbar = typer.progressbar(
            iterable=iterable, label='scan', show_pos=True, file=sys.stderr
        )
    with progressbar as iterable:
        for hit in iterable:
            file_output.write(json_obj_to_line(hit))


@app.command(name='q')
def perform_request(
    host: t.Annotated[str, typer.Argument(help='Elasticsearch host')] = 'localhost',
    #
    method: t.Annotated[
        str, typer.Option('-X', '--method', '--request', help='HTTP method')
    ] = 'GET',
    path: t.Annotated[str, typer.Option('-P', '--path', help='HTTP path')] = '/',
    _headers: t.Annotated[
        t.Optional[list[dict]],
        typer.Option('-H', '--header', parser=parse_header, help='HTTP headers'),
    ] = None,
    _params: t.Annotated[
        t.Optional[list[dict]],
        typer.Option('-p', '--params', parser=parse_params, help='HTTP params'),
    ] = None,
    #
    file_input_body: t.Annotated[t.Optional[typer.FileText], typer.Option('-d', '--data')] = None,
    file_output: t.Annotated[typer.FileTextWrite, typer.Option('-o', '--output')] = t.cast(
        typer.FileTextWrite, sys.stdout
    ),
):
    client = es.Client(host=host)
    if not path.startswith('/'):
        path = '/' + path
    headers = merge_dicts(_headers)
    params = merge_dicts(_params)
    response = client.transport.perform_request(
        method=method,
        url=path,
        headers=headers,
        params=params,
        body=file_input_body and file_input_body.read(),
    )
    file_output.write(json_obj_to_line(response))


@app.command(name='t')
def streaming_bulk_(
    host: t.Annotated[str, typer.Argument(help='Elasticsearch host')] = 'localhost',
    #
    handler: t.Annotated[
        t.Callable[[t.Iterable[str]], t.Iterable[str]],
        typer.Option(
            '-H',
            '--handler',
            parser=import_from_string,
            help='Handler class. e.g. esqt:ActionHandler',
        ),
    ] = t.cast(t.Callable[[t.Iterable[str]], t.Iterable[str]], 'esqt:ActionHandler'),
    #
    chunk_size: t.Annotated[int, typer.Option('--chunk-size')] = 500,
    max_chunk_bytes: t.Annotated[int, typer.Option('--max-chunk-bytes')] = 100 * 1024 * 1024,
    raise_on_error: t.Annotated[bool, typer.Option(' /--no-raise-on-error')] = True,
    raise_on_exception: t.Annotated[bool, typer.Option(' /--no-raise-on-exception')] = True,
    max_retries: t.Annotated[int, typer.Option('--max-retries')] = 3,
    initial_backoff: t.Annotated[int, typer.Option('--initial-backoff')] = 2,
    max_backoff: t.Annotated[int, typer.Option('--max-backoff')] = 600,
    #
    file_input_bulk_body: t.Annotated[typer.FileText, typer.Option('-d', '--data')] = t.cast(
        typer.FileText, sys.stdin
    ),
    file_output: t.Annotated[typer.FileTextWrite, typer.Option('-o', '--output')] = t.cast(
        typer.FileTextWrite, sys.stdout
    ),
    #
    progress: t.Annotated[bool, typer.Option(' /-S', ' /--no-progress')] = True,
):
    client = es.Client(host=host)
    with redirect_stdout(sys.stderr):
        print(client)
        print('waiting for seconds to start', end=' ', flush=True)
        for i in range(5, -1, -1):
            print(i, end=' ', flush=True)
            time.sleep(1)
    actions = handler(file_input_bulk_body)
    iterable = streaming_bulk(
        client=client,
        actions=actions,
        chunk_size=chunk_size,
        max_chunk_bytes=max_chunk_bytes,
        raise_on_error=raise_on_error,
        raise_on_exception=raise_on_exception,
        max_retries=max_retries,
        initial_backoff=initial_backoff,
        max_backoff=max_backoff,
        yield_ok=True,
    )
    progressbar = nullcontext(iterable)
    if progress:
        progressbar = typer.progressbar(
            iterable=iterable, label='streaming_bulk', show_pos=True, file=sys.stderr
        )
    with progressbar as iterable:
        success, failed = 0, 0
        for ok, item in iterable:
            if not ok:
                with redirect_stdout(sys.stderr):
                    print(f'Failed to index {item}')
                file_output.write(json_obj_to_line(item))
                failed += 1
            else:
                file_output.write(json_obj_to_line(item))
                success += 1
    with redirect_stdout(sys.stderr):
        print()
        print(f'{success = }')
        print(f'{failed = }')


def main():
    sys.path.insert(0, str(Path.cwd()))
    app()


if __name__ == '__main__':
    main()

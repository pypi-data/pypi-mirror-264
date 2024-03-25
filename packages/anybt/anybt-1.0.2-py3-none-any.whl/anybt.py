import argparse
import requests
from typing import List
from rich.console import Console
from rich.table import Table
from rich.align import Align
from rich.tree import Tree
from parse import *


def format_file_size(size_bytes):
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes // 1024} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes // (1024 * 1024)} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"


def get_icon(c):
    icons = {
        'ads': ':speaker_medium_volume:',
        'video': ':movie_camera:',
        'document': ':green_book:',
        'music': ':musical_note:',
        'software': ':laptop_computer:',
        'image': ':art:'
    }
    return icons.get(c, ':rocket:')


def query_string_prepare(queries: list):
    query_string = []
    for query in queries:
        query_string.append(str(query))

    rst = " ".join(query_string)
    return rst


def highlight_prepare(fields: List[str]):
    place_hold = ",".join(["\"{}\""] * len(fields))
    option = """{"highlight":{ "style":"html","fields":[""" + place_hold.format(*fields) + """]}}"""
    option = option.translate({ord('"'): "\""})
    return "/*+ SET_VAR(full_text_option='%s')*/" % option


def get_sql(args):
    query = args.file
    queries = ["{}:{}^{}".format("file_name", "\"" + query + "\"", 1.0)]
    query_str = query_string_prepare(queries)
    highlight = highlight_prepare(["file_name"])

    order_type = get_order_type(args.order)
    filter_type = get_filter_type(args.filter)

    if filter_type == 'all':
        sql = prepare_sql(
            "select {} _id ,category ,file_name ,firstadd_utc_timestamp ,filesize ,total_count from library.dht where query_string_recency(%s) ".format(
                highlight), [query_str])
    else:
        query_str = [query_str, filter_type]
        sql = prepare_sql(
            "select {} _id ,category ,file_name ,firstadd_utc_timestamp ,filesize ,total_count from library.dht where query_string_recency(%s) and category=%s ".format(
                highlight), query_str)

    if order_type == 'none':
        sql += "limit 0,{}".format(args.limit)
    else:
        sql += "order by {} desc limit 0,{}".format(order_type, args.limit)

    return sql


def get_filter_type(filter_type):
    ftypes = {
        'video': 'video',
        'ads': 'ads',
        'document': 'document',
        'music': 'music',
        'image': 'image',
        'software': 'software',
        'package': 'package'
    }

    return ftypes.get(filter_type, 'all')


def get_order_type(order_type):
    otypes = {
        'hot': 'total_count',
        'size': 'filesize',
        'date': 'firstadd_utc_timestamp'
    }
    return otypes.get(order_type, 'none')


def query(args):
    sql = get_sql(args)
    endpoint = "https://gateway.magnode.ru/blockved/glitterchain/index/sql/simple_query"
    req = {"sql": sql, "arguments": []}
    r = requests.post(endpoint, json=req, timeout=10)
    if r.status_code != 200:
        return
    rst = r.json()
    return rst


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str, required=True,
                        help='Please enter the desired file name for searching.')
    parser.add_argument('-l', '--limit', type=int, default=20,
                        help='The number of results you would like to display.')
    parser.add_argument('-o', '--order', type=str, default='none',
                        help='The order of results you would like to display.')
    parser.add_argument('-ft', '--filter', type=str, default='all',
                        help='The type of results you would like to display.')

    args = parser.parse_args()

    rst = query(args)

    console = Console()
    table = Table(show_header=True, header_style="bold magenta", expand=True)
    table_centered = Align.center(table)
    link = "You could also try a web version running on ENS & IPFS:\n https://anybt.eth.limo"
    table.add_column(link)
    table.add_column("ext", style="dim", no_wrap=True)

    for row in rst['result']:
        row = row['row']
        category = get_icon(row["category"]["value"]) + "  " + row["category"]["value"]
        ext = Tree(category)
        ext.add(format_file_size(float(row["filesize"]["value"])))
        ext.add("{} Hot".format(int(float(row["total_count"]["value"]))))
        ext.add(time.strftime("%Y-%m-%d", time.localtime(float(row["firstadd_utc_timestamp"]["value"]))))

        content = Tree(row["_highlight_file_name"]["value"].replace("<mark>", "[red]").replace("</mark>", "[/red]"))
        magnet_link = "magnet:?xt=urn:btih:{}".format(row["_id"]["value"])
        content.add(magnet_link)

        table.add_row(content, ext)

    console.print(table)


if __name__ == '__main__':
    main()

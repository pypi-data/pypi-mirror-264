#!/usr/bin/env python3
import argparse
from glitter_sdk.client.lcd import LCDClient
from glitter_sdk.core import Numeric, Coins
from glitter_sdk.key.mnemonic import MnemonicKey
from glitter_sdk.util.parse_sql import prepare_sql
from glitter_sdk.util.parse_query_str import *
from rich.console import Console
from rich.table import Table
from rich.align import Align
from rich.tree import Tree
from glitter_sdk.util.highlight import *
import time


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


def get_sql(args):
    query = args.file
    queries = [MatchPhraseQuery("file_name", query, 1.0)]
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

    mnemonic = ""
    mk = MnemonicKey(mnemonic)
    client = LCDClient(
        chain_id="glitter_12000-2",
        url="https://gateway.magnode.ru",
        gas_prices=Coins.from_str("1agli"),
        gas_adjustment=Numeric.parse(1.5))
    glitter_db_client = client.db(mk)
    sql = get_sql(args)
    rst = glitter_db_client.query(sql)

    console = Console()
    table = Table(show_header=True, header_style="bold magenta", expand=True)
    table_centered = Align.center(table)
    link = "You could also try a web version running on ENS & IPFS:\n https://anybt.eth.limo"
    table.add_column(link)
    table.add_column("ext", style="dim", no_wrap=True)

    for row in rst:
        category = get_icon(row["category"]) + "  " + row["category"]
        ext = Tree(category)
        ext.add(format_file_size(row["filesize"]))
        ext.add("{} Hot".format(int(row["total_count"])))
        ext.add(time.strftime("%Y-%m-%d", time.localtime(row["firstadd_utc_timestamp"])))

        content = Tree(row["_highlight_file_name"].replace("<mark>", "[red]").replace("</mark>", "[/red]"))
        magnet_link = "magnet:?xt=urn:btih:{}".format(row["_id"])
        content.add(magnet_link)

        table.add_row(content, ext)

    console.print(table)


if __name__ == '__main__':
    main()

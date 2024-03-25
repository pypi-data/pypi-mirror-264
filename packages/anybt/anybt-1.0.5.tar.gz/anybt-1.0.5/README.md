# AnyBT: An Open Sourced Decentralized BitTorrent Search Engine

Introducing AnyBT, a tool for searching magnet link of all kinds of BitTorrent contents. It's based on a decentralized data protocol - [Glitter Protocol](https://twitter.com/GlitterProtocol).

You could use AnyBT to search for magnet links base on file names and displays search results with a simple interface.

There is also [a web version of AnyBT](https://anybt.eth.limo) works on [ENS](https://ens.domains/) and [IPFS](https://ipfs.tech/) available if you do not have Python environment.

## Getting Started

To get started, please follow these steps:

### Prerequisites

- Python (v3.7 or higher)

### Installation

Installing the tool, and you should make sure `your/download/path` in the `$PATH`, then you can use the command line tool.

```shell
pip install anybt
``` 

### Options

- `terms`:Specifies search terms to be queried. Required:yes.

- `-p <page>` or `--page <page>`:Specifies the page of results to display. Default: 0.

- `-l <limit>` or `--limit <limit>`:Specifies the number of per page to display. Default: 10.

- `-s <sort type>` or `--sort <sort type>`:Specifies the sorting sequence of results to display. Default: none.
    - `hot` :sort by the file heat
    - `size` :sort by the size of file
    - `date` :sort by the original publication time of the file

- `-t <filter type>` or `--type <fliter type>`:Specifies the category of result to display. Default: all.
    - `video` :video categories.
    - `document`:document categories.
    - `image` :image categories.
    - `music` :music categories.
    - `software` :software categories.
    - `package` :package categories.

### Examples

1. Search for keyword "Chaplin":

```shell
anybt  Chaplin
```

2. Search for keywords "Charlie Chaplin" and page 1, limit 5:

```shell
anybt  "Charlie Chaplin" -p 1 -l 5 
```

3. Search for keywords "Charlie Chaplin" and order by file size:

```shell
anybt  "Charlie Chaplin" -s size 
```

4. Search for keywords "Charlie Chaplin" and only keep the video resource:

```shell
anybt "Charlie Chaplin" -t video
```

## Built With

- [glitter-sdk-py](https://github.com/glitternetwork/glitter-sdk-py) A Python SDK for interacting with the Glitter Protocol.

## Contributing

If you would like to contribute to this project, feel free to fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License - see the LICENSE file for details.


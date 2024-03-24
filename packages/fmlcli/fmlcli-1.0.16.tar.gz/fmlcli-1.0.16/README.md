# A Magnet Search Tool 

This project is a tool for searching magnet links. It is built based on a decentralized search engine. 
It allows users to search for magnet based on the file name and displays the search results in a simple interface.

## Getting Started

To get started with this project, follow these steps:

### Prerequisites

- Python (v3.8 or higher)

### Installation

Installing the tool, and you should make sure `your/download/path` in the `$PATH`, then you can use the command line tool.

```shell
pip install fmlcli
``` 

### Options

- `-f <filename>` or `--file <filename>`:Specifies the filename to be processed. The -f or --file option is must 

- `-l <resultlimit>` or `--limit <resultlimit>`:Specifies the number of results to display. This is an optional parameter with a default value of 10.

- `-o <order type>` or `--order <order type>`:Specifies the ordering sequence of results to display. This is an optional parameter with a default value of 'none'
  - `hot` or `heat` :order by the file heat
  - `size` or `filesize` :order by the size of file
  - `date` or `time` :order by the original publication time of the file

- `-ft <filter type>` or `--fliter <fliter type>`:Specifies the category of result to display. This is an optional parameter with a default value of 'all'
  - `video` or `movie` or `film` :video categories.
  - `document` or `file` :document categories.
  - `picture` or `image` :image categories.
  - `ads` :ads categories.
  - `music` :music categories.
  - `software` :software categories.
  - `package` :package categories.

### Example

Search for files named 'Freelance' that are categorized as 'video' and display the top 5 results sorted by hot.

```shell
fmlcli -f Freelance -l 5 -o hot -ft vedio
```

## Built With

- [glitter-sdk-py](https://github.com/glitternetwork/glitter-sdk-py) a blockchain-based data platform to help applications store, manage and elevate the world’s data in Web3 way.

## Contributing

If you would like to contribute to this project, feel free to fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License - see the LICENSE file for details.


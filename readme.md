## RACCOON

Raccoon is web page downloader.

This script will download whole online html page; includes its css, js, images and fonts.  
It is really useful when you want to download a single page html theme.

### Requirements

- Python3
- BeautifulSoup
- Requests

### Installation

```
$ pip3 install -r requirements.txt
$ python3 raccoon.py --help 
```

### Usage

Example Usage:

```
$ python3 raccoon.py -u http://example.com
$ python3 raccoon.py -u http://example.com -i index.html
$ python3 raccoon.py -u http://example.com -i index.html -o site-files
```

NOTE: "-u/--url" parameter must define the base address which all css, js and the other files take as base address.

Advanced Usage:

```
usage: raccoon.py [-h] -u  [-i] [-o]

Single page html downloader

optional arguments:
  -h, --help      show this help message and exit
  -u , --url      Html url base address
  -i , --index    Html path
  -o , --output   User username

NOTE:
    "--url" parameter must define the base address which all css, js and the other files take as base address.

EXAMPLE USAGE:
    python3 raccoon.py -u http://example.com
    python3 raccoon.py -u http://example.com -i index.html
    python3 raccoon.py -u http://example.com -i index.html -o site-files
```
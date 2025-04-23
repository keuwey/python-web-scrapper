# Python Web Scrapper

A simple python web scrapper made to consolidate my learning

## How it works

The web scrapper goes to a government site and downloads two PDF's called "Anexo I" and "Anexo II" and then it zips them together.

## Tech Stack

- Requests (To manage HTTP requests)
- BeautifulSoup 4 (To deal with the scrapping part)
- Zipfile (To zip the downloaded files)
- Pathlib (To deal with absolute and relative paths)
- Datetime (To deal with dates)

## How to run:

First, clone the repository:

```bash
git clone https://github.com/keuwey/python-web-scrapper.git
```

Then go to the directory:

```bash
cd python-web-scrapper
```

And then just run the main file with the python interpreter:

```bash
python app.py
```

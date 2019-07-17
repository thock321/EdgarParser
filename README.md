# Edgar Parser

An SEC Edgar parser that can parse mutual fund holdings and print them to a tab-separated file.

## Getting Started

### Prerequisites

Run 

```
pip install -r requirements.txt
```

To get all required libraries installed.

## Running tests

Simply run `test.py` to test functionality.  It will parse a list of pre-determined CIKs and output them to tab-separated files.

## Usage

First we need to import `EdgarParser`

```
from EdgarParser import EdgarParser
```

Here is an example to create an instance of an `EdgarParser` with a specified CIK:

```
CIK = '0001166559'
ep = EdgarParser(cik=CIK)
```

By default, `EdgarParser` will get the latest mutual fund holdings data occurrence.  For example, if fund XXX's last reported holdings was on 5/30/2017, then EdgarParser will get the holdings reported on 5/30/2017 instead of the latest filing date.
If you only want mutual fund holdings from the latest 13F filing, then specify `get_last_holding` to be FALSE.

```
CIK = '0001166559'
ep = EdgarParser(cik=CIK, get_last_holding=False)
```

`EdgarParser` also supports tickers in place of CIKs.  Simply use a ticker in place of a CIK in the `cik` argument.

```
tckr = 'BLK'
ep = EdgarParser(cik=tckr)
```

If you want to get holdings before a certain date, simply specify it in the form of 'YYYYMMDD'.

```
#Get holdings on or before May 30, 2019
ep = EdgarParser(cik=CIK, date_before='20170530')
```

Now to get the URL for the XML with all of the holdings data, we can simply call `get_latest_file`.

```
ep.get_latest_file()
```

To print the holdings data to a tab-separated file, simply call `fund_holdings_to_tsv`.

```
ep.fund_holdings_to_tsv()
```

Your code should look something like this

```
from EdgarParser import EdgarParser

CIK = '12345'

ep = EdgarParser(cik=CIK)

ep.fund_holdings_to_tsv()
```

## Features

`EdgarParser.parse()` parses an XML into an `ElementTree` from a URL.

`EdgarParser.get_filing_page()` Gets the page with all filings of the specified type.

`EdgarParser.get_latest_file()` Gets the latest holdings reported.

`EdgarParser.fund_holdings_to_tsv()` Outputs the latest holdings to a tab-separated file.

## Extra Notes

### Thought Process

The first thing I did after receiving this assignment was search on Google whether or not there were any existing libraries that parse from Edgar.  To my suprise, there was actually more than one.  However, I tested a couple and didn't feel that they suited my needs.  Therefore, I would have to write my own functions to handle the requirements

First of all, I needed a way to parse an XML file.  Python has a built in library, so that's what I used.  Next, I decided to use the `requests` library and `BeautifulSoup` library to connect to and parse web pages.  Now I had all the tools I needed.

After doing a few searches on Edgar, I realized that the search URL contained arguments for search parameters.  Then, I looked at the page source for 13F filings.  All the links to the filings were id'ed, so I simply needed to get a list of links with that id.  Then, I would just need to find the link in the resulting page that led to the XML file we needed.

To create the tab-separated file, I simply used the built in csv library, and changed the delimiter from a comma to a tab.  I looked at the XML file formats, and realized that some columns were not always used.  I added a manual check to make sure that if the column did not exist, 'N/A' would be written instead.

I realized that some funds, such as BlackRock's, did not have the XML file with all of the holdings.  After looking at more past filings, I realized that they stopped providing the holdings after a certain point.  This is why I added the `get_last_holding` functionality.  However, the holdings that this produces may not be up to date, which is why the functionality can be turned off.

Overall, this was a fun project and I hope I did well.  This is actually the first time I created something like this, so I really appreciate any feedback or constructive criticism on what I can do better.

### Edge Cases Tested

Case 1: Invalid CIK

Result

```
EdgeParser('123').fund_holdings_to_tsv()
>There is no holding data for CIK=123
```

Case 2: Ticker with no 13F filings

Result

```
EdgeParser('AAPL').fund_holdings_to_tsv()
>There is no holding data for CIK=AAPL
```
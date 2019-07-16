# Edgar Parser

An SEC Edgar parser that can parse mutual fund holdings and print them to a tab-separated file.

## Getting Started

### Prerequisites

```
BeautifulSoup 4
```

## Running tests

Simply run `EdgarParser.py` to test functionality.  It will parse a list of pre-determined CIKs and output them to a tab-separated file.

## Usage

Here is an example to create an instance of an `EdgarParser` with a specified CIK:

```
ep = EdgarParser(cik=CIK)
```

By default, `EdgarParser` will get the latest mutual fund holdings data occurrence.  For example, if fund XXX last reported holdings was on 5/30/2017, then EdgarParser will get the holdings reported on 5/30/2017 instead of the latest filing date.
If you only want mutual fund holdings from the latest 13F filing, then specify `get_last_holding` to be FALSE.

```
ep = EdgarParser(cik=CIK, get_last_holding=False)
```

If you want to get holdings before a certain date, simply specify it in the form of 'YYYYMMDD'.

```
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

## Features

`EdgarParser.parse()` parses an XML into an `ElementTree` from a URL.

`EdgarParser.get_filing_page()` Gets the page with all filings of the specified type.

`EdgarParser.get_latest_file()` Gets the latest holdings reported.

`EdgarParser.fund_holdings_to_tsv()` Outputs the latest holdings to a tab-separated file.
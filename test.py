from EdgarParser import EdgarParser
    
ciks = ['0001756111', '0001166559', '0001555283', '0001397545', '0001543160', '0001496147', '0001357955', '0001439289', '0001086364']


for cik in ciks:
    ep = EdgarParser(cik=cik, get_last_holding=True)
    ep.fund_holdings_to_tsv()


EdgarParser(cik='BLK').fund_holdings_to_tsv()

import xml.etree.ElementTree as ET
import requests
import re
import csv
import datetime as dt

from bs4 import BeautifulSoup

def get_base_url():
    return 'https://www.sec.gov'

def get_13f_ns():
    return '{http://www.sec.gov/edgar/document/thirteenf/informationtable}'

class EdgarParser:

    '''
    cik is the cik of our fund.

    date_before is the date set such that we find the earliest filing before or on this date.

    get_last_holding is true if we want the latest holding data that was posted.  Some filings, such as BlackRock's, does not having holding data
    for later dates.  Therefore, if we set get_last_holding to True, then it means we will search for the last time the holding data was posted.
    If we set it to false, then get_latest_file throws an exception if no holding data can be found.
    '''
    def __init__(self, cik, file_type='13F', date_before='', get_last_holding=True):
        self.cik = cik
        self.file_type = file_type
        self.date_before = date_before
        self.get_last_holding = get_last_holding

    '''
    Parse a xml URL into an ElementTree
    '''
    def parse(self, url):
        request = requests.get(url)
        root = ET.fromstring(request.text)
        return root

    def get_filing_page(self):
        return 'https://www.sec.gov/cgi-bin/browse-edgar?CIK=' + self.cik + '+&type=' + self.file_type + '&dateb=' + self.date_before + '&owner=exclude&action=getcompany&Find=Search'

    '''
    Get the latest xml URL that contains our holding data.
    '''
    def get_latest_file(self):
        url = self.get_filing_page()
        request = requests.get(url)
        soup = BeautifulSoup(request.text, 'html.parser')
        xml_url = ''

        #From looking at the html source, all the relevant document links have the id 'documentsbutton'
        doc_urls = soup.find_all('a', {'id': 'documentsbutton'})

        #Find last holding data
        if self.get_last_holding:
            for doc_url in doc_urls:
                url = get_base_url() + doc_url['href']
                request = requests.get(url)
                soup = BeautifulSoup(request.text, 'html.parser')
                for link in soup.find_all('a'):
                    if 'primary_doc' not in link.text and '.xml' in link.text:
                        xml_url = link['href']
                #If we found the holding data, break out of the loop
                if xml_url != '':
                    break
                
        #Find holding data on the latest filing only.  Do not look through previous filing dates.
        else:
            #Get first occurrence of document since that is always the latest
            url = get_base_url() + doc_urls[0]['href']
            request = requests.get(url)
            soup = BeautifulSoup(request.text, 'html.parser')
            
            for link in soup.find_all('a'):
                #The last xml link is the 'xml' page and not the 'html' page
                if 'primary_doc' not in link.text and '.xml' in link.text:
                    xml_url = link['href']
        if xml_url == '':
            raise Exception('No holding data found.')
        return get_base_url() + xml_url

    '''
    Write holding data to a tab seperated file.
    '''
    def fund_holdings_to_tsv(self):
        url = ''
        try:
            url = self.get_latest_file()
        except:
            print('There is no holding data for CIK=' + self.cik)
            return
        root = self.parse(url)
        date = self.date_before
        if date == '':
            now = dt.datetime.now().strftime('%Y%m%d')
            date = now
            
        with open('./' + self.cik + '_' + date + '_output.tsv', 'wt') as out:
            tw = csv.writer(out, delimiter='\t')
            #Write our column names first
            tw.writerow(['Issuer', 'Title of Class', 'CUSIP Number', 'Market Value', 'Amount of Security', 'Type of Security', \
                                 'Put/Call', 'Investment Discretion', 'Other Managers', 'Voting Authority Sole', 'Voting Authority Shared', 'No Voting Authority'])
            
            for info_table in root:
                #col keeps track of what column we are writing on
                col = 0
                row = []
                for child in info_table:
                    #print(child.tag)
                    if col == 6:
                        #Check for putCall existence.  
                        if child.tag != get_13f_ns() + 'putCall':
                            row.append('N/A')
                            col += 1
                    elif col == 8:
                        #check for otherManager existence
                        if child.tag != get_13f_ns() + 'otherManager':
                            row.append('N/A')
                            col += 1
                    if child.tag == get_13f_ns() + 'shrsOrPrnAmt' or child.tag == get_13f_ns() + 'votingAuthority':
                        for sub_child in child:
                            row.append(sub_child.text)
                            col += 1
                        continue
                    row.append(child.text)
                    col += 1
                tw.writerow(row)

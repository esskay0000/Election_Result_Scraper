# -*- coding: utf-8 -*-
"""
Created on Tue May 28 10:39:45 2019

@author: Pratik
"""

import pandas as pd
from bs4 import BeautifulSoup
import requests

base_url = 'http://results.eci.gov.in/pc/en/'
base_url += 'constituencywise/Constituencywise'

state_ids = ['S' + '{0:0=2d}'.format(x) for x in range(1, 30)]
ut_ids = ['U' + '{0:0=2d}'.format(x) for x in range(1, 8)]
all_const_ids = state_ids + ut_ids
all_data = []

for const_id in all_const_ids:
    for iter_ in range(1, 100):
        url = base_url + const_id + str(iter_)
        url += '.htm?ac=' + str(iter_)
        text = requests.get(url).text
        soup = BeautifulSoup(text, 'lxml')
        tab = soup.find("table", {"class":"table-party"})

        if not tab:
            print ('%s constituencies in %s' %(iter_-1, const_id))
            break
        
        table_rows = tab.find_all('tr')
        l = []
        for tr in table_rows[3:-1]:
            td = tr.find_all('td')
            row = [tr.text for tr in td]
            l.append(row)
            
        if len(row) == 8:
            colnames = ['O.S.N.', 'Candidate', 'Party', 'EVM Votes', 'Migrant Votes',
                        'Postal Votes', 'Total Votes', '% of Votes']
        else:
            colnames = ['O.S.N.', 'Candidate', 'Party', 'EVM Votes',
                        'Postal Votes', 'Total Votes', '% of Votes']
            
        l = pd.DataFrame(l, columns = colnames)
        l['Constituency'] = table_rows[0].text.strip()
        all_data.append(l)
        
output = pd.concat(all_data, sort = False)
state_const_names = pd.DataFrame(output.Constituency.str.split('-', 1).tolist(), columns = ['State', 'Constituency'])
output = pd.concat([output.drop(['Constituency'], axis = 1).reset_index(), state_const_names], axis = 1)
output.to_excel('C:\\Users\\Pratik\\Desktop\\Mamaji\\output.xlsx')
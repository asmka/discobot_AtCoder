""" atcoder """
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup

CONTEST_URL = 'https://atcoder.jp/contests/?lang=ja'

def _get_context_tag_list(url: str):
    """ get_context_tags """
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    plan_tag = soup.find('h3', text='予定されたコンテスト').find_next_sibling()
    ctags = plan_tag.find('tbody').find_all('tr')
    return ctags

def get_contest_plan():
    """ get_contest_plan """
    ctags = _get_context_tag_list(CONTEST_URL)
    # Parse tag list
    cplan = []
    for tag in ctags:
        # Extract elements
        elems = []
        for string in tag.stripped_strings:
            elems.append(string)
        if len(elems) != 4:
            raise Exception
        # Format elements
        start_time = datetime.strptime(elems[0], '%Y-%m-%d %H:%M:%S%z')
        name = elems[1]
        hours, minutes = map(int, elems[2].split(':'))
        rate = elems[3]
        intervals_min = hours*60 + minutes
        end_time = start_time + timedelta(minutes=intervals_min)
        # Pack required information
        cplan.append({
            'start_time': start_time,
            'end_time': end_time,
            'name': name,
            'rate': rate
        })
    return cplan

""" atcoder """
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup

CONTEST_URL = 'https://atcoder.jp/contests/?lang=ja'
WEEK_LIST = ['月', '火', '水', '木', '金', '土', '日']

def _convert_week_knj(week_id: int):
    """ convert_week_knj """
    if week_id > len(WEEK_LIST):
        raise Exception
    return WEEK_LIST[week_id]

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
        contest_name = elems[1]
        hours, minutes = map(int, elems[2].split(':'))
        target_rate = elems[3]
        # Calculate contest time
        intervals_min = hours*60 + minutes
        end_time = start_time + timedelta(minutes=intervals_min)
        week_knj = _convert_week_knj(start_time.weekday())
        contest_time = start_time.strftime('%Y-%m-%d') + \
                       '(' + week_knj + ')' + \
                       start_time.strftime('%H:%M') + '~' + \
                       end_time.strftime('%H:%M')
        # Pack required information
        cplan.append({
            'time': contest_time,
            'name': contest_name,
            'rate': target_rate
        })
    return cplan

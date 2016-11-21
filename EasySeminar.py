#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
EasySeminar : A tool to make graduate easy again!

自动读取新版网络学堂文化素质教育讲座通知并生成iCal文件供Calendar应用使用

Author        : Yongwen Zhuang
Created       : 2016-11-19
Last Modified : 2016-1-19
'''

from bs4 import BeautifulSoup
import re
import os
import time
import json
import requests
import datetime
import icalendar

import logging

from user import username, password

_FORMAT = '%(asctime)-15s %(message)s'
_DebugLevel = logging.INFO
logging.basicConfig(level=_DebugLevel, format=_FORMAT)
logger = logging.getLogger(__name__)

_session = requests.session()
_URL_LOGIN = 'https://id.tsinghua.edu.cn/do/off/ui/auth/login/post/fa8077873a7a80b1cd6b185d5a796617/0?/j_spring_security_thauth_roaming_entry'
_URL = 'http://learn.cic.tsinghua.edu.cn/b/myCourse/notice/listForStudent/2016-2017-1-00690651-90?currentPage=1&pageSize=150&_={}'

def login():
    """
    login to get cookies in _session
    :return:True if succeed
    """
    data = dict(
        i_user=username,
        i_pass=password,
    )
    r = _session.post(_URL_LOGIN, data)

def get():
    """
    _session.GET the page, handle the encoding and return the BeautifulSoup
    :param url: Page url
    :return: BeautifulSoup
    """
    r = _session.get(_URL)
    r.encoding = 'utf-8'
    return r.content

def parse_time(string):
    """
    parse time of string
    :string: string with time format 'yyyy年mm月dd日（周几）HH：MM'
    :returns: datetime.datetime
    """
    try:
        (y,m,d,h,M) = re.findall('[0-9]+', string)[:5]
    except:
        (y,m,d,h) = re.findall('[0-9]+', string)[:4]
        M = 0
    if '晚' in string or '下午' in string:
        h = int(h)
        h = h + 12 if h < 12 else h;
    dtstart = datetime.datetime(int(y), int(m), int(d), int(h), int(M))
    dtend = dtstart+datetime.timedelta(seconds = 90*60)
    return [dtstart, dtend]


def event_c(record):
    """
    create event use record
    :record: content of notice
    :returns: icalendar.Event
    """
    event = icalendar.Event()
    event['description'] = ''
    event['uid'] = record['id']
    event['summary'] = record['title']
    notice = BeautifulSoup(record['detail'], 'html.parser')
    for line_soup in notice('p'):
        line = line_soup.text
        event['description'] += line+'\n'
        line = line.replace('\xa0','')
        line = line.replace(' ','')
        if '演讲题目' == line[:4]:
            event['summary'] = line[5:]
        if '时间' == line[:2] or '日期' == line[:2]:
            (dtstart, dtend) = parse_time(line[3:])
            event.add('dtstart', dtstart)
            event.add('dtend', dtend)
        if '地点' == line[:2]:
            event['location'] = line[3:]
    if event.has_key('dtstart'):
        return event
    return None

def test():
    """
    test! read message from txt
    """
    with open('res.txt', 'r') as f:
        s = f.read()
    res = json.loads(s)['paginationList']
    return res

def get_res():
    login()
    return json.loads(get().decode('utf8'))['paginationList']

if __name__ == "__main__":
    event_len = 0
    cal = icalendar.Calendar()
    cal['prodid'] = '-//EasySeminar//ZH'
    cal['version'] = '2.0'
    cal['x-wr-calname'] = '学校讲座信息'
    cal['x-wr-timezone'] = 'Asia/Shanghai'
    cal['x-wr-caldesc'] = '网络学堂讲座信息'
    # res = test()
    res = get_res()
    # dict_keys(['pageMax', 'currentPageStr', 'pageStart', 'recordCount', 'recordCountStr', 'pageSize', 'recordList', 'currentPage'])
    # res keys
    for record in res['recordList']:
        event = event_c(record['courseNotice'])
        if event is not None:
            cal.add_component(event)
            event_len += 1
    logger.info("Receive {} notices".format(event_len))
    with open('test.ics', 'wb') as f:
        f.write(cal.to_ical())

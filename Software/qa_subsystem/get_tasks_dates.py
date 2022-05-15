#!/usr/bin/env python3
# Gets and parses the Tasks and Due Dates table from the wiki page
# https://designlab.eng.rpi.edu/edn/projects/capstone-support-dev/wiki/Tasks_and_Due_Dates
# Running this program as __main__ serializes and saves the data to JSON files
# in storage/rules/ and pretty-prints the parsed entries

import requests
import re
import datetime
import json
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from enum import Enum, IntEnum, auto
from pydantic import BaseModel
from typing import List


# If the table's columns on the wiki page are ever changed, fixing this enum
# should suffice
class TableCols(IntEnum):
    NAME = 0
    TEAM_INDV = auto()
    WIKI = auto()
    RUBRIC = auto()
    DATE = auto()

# Different date formats found in the TableCols.DATE-th column of the table
class DateStyle(IntEnum):
    NONE = auto() # Cell contains no dates
    DATE = auto() # A single date
    DATE2 = auto() # 2 separate dates
    TIME = auto() # Date and time
    RANGE = auto() # Date range

class Class(BaseModel):
    name: str = ''
    wiki: List[str] = []
    agenda: str = ''
    date_style: DateStyle = DateStyle.NONE
    date1: datetime.date = None
    date2: datetime.date = None
    date_str: str = ''
    def __str__(self):
        ret = self.name + ' on ' + self.date_str + '\nAgenda: ' + self.agenda + '\n'
        if self.wiki:
            ret += 'Wiki pages:\n'
            for link in self.wiki:
                ret += '  ' + link + '\n'
        return ret
    def to_json_dict(self):
        d = self.__dict__
        d['date_style'] = d['date_style'].value
        if d['date1']: d['date1'] = d['date1'].toordinal()
        if d['date2']: d['date2'] = d['date2'].toordinal()
        return d
    @classmethod
    def from_json_dict(cls, d):
        ret = Class()
        ret.name = d['name']
        ret.wiki = d['wiki']
        ret.agenda = d['agenda']
        ret.date_style = DateStyle(d['date_style'])
        if d['date1']: ret.date1 = datetime.date.fromordinal(d['date1'])
        else:                   ret.date1 = None
        if d['date2']: ret.date2 = datetime.date.fromordinal(d['date2'])
        else:                   ret.date2 = None
        ret.date_str = d['date_str']
        return ret

class Assignment(BaseModel):
    name: str = ''
    graded: bool = False
    team: bool = False
    indv: bool = False
    wiki: List[str] = []
    rubric: List[str] = []
    due_style: DateStyle = DateStyle.NONE
    due1: datetime.date = None
    due2: datetime.date = None
    due_time: datetime.time = None
    due_str: str = ''
    def __str__(self):
        ret = self.name + ': '
        if self.graded:
            ret += 'graded '
        if self.team:
            ret += 'team'
            ret += '/individual ' if self.indv else ' '
        elif self.indv:
            ret += 'individual '
        ret += 'assignment\n'
        if self.wiki:
            ret += 'Instructions can be found here:\n'
            for link in self.wiki:
                ret += '  ' + link + '\n'
        if self.rubric:
            ret += 'Rubrics:\n'
            for link in self.rubric:
                ret += '  ' + link + '\n'
        return ret + 'Due ' + self.due_str
    def to_json_dict(self):
        d = self.__dict__
        d['due_style'] = d['due_style'].value
        if d['due1']: d['due1'] = d['due1'].toordinal()
        if d['due2']: d['due2'] = d['due2'].toordinal()
        if d['due_time']: d['due_time'] = d['due_time'].isoformat()
        return d
    @classmethod
    def from_json_dict(cls, d):
        ret = Assignment()
        ret.name = d['name']
        ret.graded = d['graded']
        ret.team = d['team']
        ret.indv = d['indv']
        ret.wiki = d['wiki']
        ret.rubric = d['rubric']
        ret.due_style = DateStyle(d['due_style'])
        if d['due1']: ret.due1 = datetime.date.fromordinal(d['due1'])
        else:         ret.due1 = None
        if d['due2']: ret.due2 = datetime.date.fromordinal(d['due2'])
        else:         ret.due2 = None
        if d['due_time']: ret.due_time = datetime.time.fromisoformat(d['due_time'])
        else:             ret.due_time = None
        ret.due_str = d['due_str']
        return ret

wiki_url = 'https://designlab.eng.rpi.edu/edn/projects/capstone-support-dev/wiki/'
tasks_dates_url = wiki_url + 'Tasks_and_Due_Dates'

def get_tasks_dates():
    r = requests.get(tasks_dates_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    year = datetime.date.today().year
    team_color_def = soup.find(is_team_color_def)
    indv_color_def = soup.find(is_indv_color_def)
    team_color = re.search('background:#(.{6})', team_color_def['style'])[1]
    indv_color = re.search('background:#(.{6})', indv_color_def['style'])[1]
    graded = re.compile('background:#(' + team_color + '|' + indv_color + ')', re.I)

    table = soup.table
    if table is None:
        return
    headers = table.find_all('th')
    if len(headers) < len(TableCols.__members__):
        return
    date_sub = re.subn('[^0-9,()]', '', headers[TableCols.DATE].string)
    date_spec = date_sub[0]
    sections = re.match('(.*?)\((.*)\)', date_spec)
    normal_sec = [int(s) for s in sections[1].split(',')]
    paren_sec  = [int(s) for s in sections[2].split(',')]

    classes = []
    assignments = []
    other = []
    for row in table.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) < len(TableCols.__members__):
            continue
        name_cell = cells[TableCols.NAME]
        if name_cell.string is None:
            continue
        name = name_cell.string.strip()

        date_re = '([0-9]+).([0-9]+)'
        date_str = cells[TableCols.DATE].string
        date_style = None
        date1 = None
        date2 = None
        time = None
        if date_str is not None:
            date_str = date_str.strip()
            match = re.search(date_re + r'\s*\(\s*' + date_re + r'\s*\)', date_str)
            if match:
                date_style = DateStyle.DATE2
                date1 = datetime.date(year, int(match[1]), int(match[2]))
                date2 = datetime.date(year, int(match[3]), int(match[4]))
            else:
                match = re.search(date_re + r'\s*-\s*'+ date_re, date_str)
                if match:
                    date_style = DateStyle.RANGE
                    date1 = datetime.date(year, int(match[1]), int(match[2]))
                    date2 = datetime.date(year, int(match[3]), int(match[4]))
                else:
                    match = re.search(date_re + r'.*?([0-9]+)\s*:\s*([0-9]+)\s*(p|a)', date_str, re.I)
                    if match:
                        date_style = DateStyle.TIME
                        date1 = datetime.date(year, int(match[1]), int(match[2]))
                        time = datetime.time(int(match[3]) + (0 if match[5] == 'a' else 12), int(match[4]))
                    else:
                        match = re.search(date_re, date_str)
                        if match:
                            date_style = DateStyle.DATE
                            date1 = datetime.date(year, int(match[1]), int(match[2]))
                        else:
                            date_style = DateStyle.NONE

        team_indv = cells[TableCols.TEAM_INDV].string
        if team_indv: # This is an assignment or class
            team = bool(re.search('team',       team_indv, re.I))
            indv = bool(re.search('individual', team_indv, re.I))
            if team and re.search('in.class', name, re.I): # This is a class
                cls = Class()
                cls.name = name
                for link in cells[TableCols.WIKI].find_all('a', href=True):
                    url = urljoin(tasks_dates_url, link['href'])
                    cls.wiki.append(url)
                    r2 = requests.get(url)
                    soup2 = BeautifulSoup(r2.text, 'html.parser')
                    agenda_heading = soup2.find(is_agenda_heading)
                    if agenda_heading:
                        agenda_img = agenda_heading.find_next('img', src=True)['src']
                        cls.agenda = urljoin(tasks_dates_url, agenda_img)
                cls.date_style = date_style
                cls.date1 = date1
                cls.date2 = date2
                cls.date_str = date_str
                classes.append(cls)
            else: # This is an assignment
                assign = Assignment()
                assign.name = name
                assign.graded = bool('style' in name_cell.attrs and graded.search(name_cell['style']))
                assign.team = team
                assign.indv = indv
                for link in cells[TableCols.WIKI].find_all('a', href=True):
                    assign.wiki.append(urljoin(tasks_dates_url, link['href']))
                for link in cells[TableCols.RUBRIC].find_all('a', href=True):
                    assign.rubric.append(urljoin(tasks_dates_url, link['href']))
                assign.due_style = date_style
                assign.due1 = date1
                assign.due2 = date2
                assign.due_time = time
                assign.due_str = date_str
                assignments.append(assign)
        else:
            other.append(name)
    return (classes, assignments, other)

def is_color_def(tag):
    return (tag.name == 'span'
            and tag.string is not None
            and 'style' in tag.attrs
            and re.search('background', tag['style']))
def is_team_color_def(tag):
    return (is_color_def(tag) and re.match('team.*assignment', tag.string, re.I))
def is_indv_color_def(tag):
    return (is_color_def(tag) and re.match('individual.*assignment', tag.string, re.I))
def is_agenda_heading(tag):
    if tag.name == 'h2':
        for s in tag.contents:
            if s.string and re.match('in.class', s.string, re.I):
                return True
    return False

if __name__ == '__main__':
    classes, assignments, other = get_tasks_dates()
    with open('storage/rules/class-sessions.json', 'w') as class_f, \
         open('storage/rules/assignments.json', 'w')    as assign_f, \
         open('storage/rules/other-dates.json', 'w')    as other_f:
        json.dump([c.to_json_dict() for c in classes],     class_f)
        json.dump([a.to_json_dict() for a in assignments], assign_f)
        json.dump(other, other_f)
    with open('storage/rules/class-sessions.json', 'r') as class_f, \
         open('storage/rules/assignments.json', 'r')    as assign_f, \
         open('storage/rules/other-dates.json', 'r')    as other_f:
        print('Classes:')
        for c in json.load(class_f):
            print(Class.from_json_dict(c), '\n')
        print('\nAssignments:')
        for a in json.load(assign_f):
            assign = Assignment.from_json_dict(a)
            # if assign.graded:
            print(assign, '\n')
        print('\nOther:')
        for o in json.load(other_f):
            print(o)

#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
#
# get_cemeb_cal: Get calendar from CeMEB
# Copyright 2024 Robert Wolff <mahlzahn@posteo.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import argparse
argcomplete_available = True
try:
    import argcomplete
except ModuleNotFoundError:
    argcomplete_available = False

import datetime
import re
import uuid
import zoneinfo

import bs4
import requests
import icalendar

def parse_args():
    parser = argparse.ArgumentParser(
            prog='get_cemeb_cal',
            description='Get calendar from CeMEB',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    default_fr = datetime.date.today().strftime('%d/%m/%Y')
    parser.add_argument('-f', '--from', dest='fr', default=default_fr,
                        help='date from which to search for in form of d/m/Y')
    parser.add_argument('-t', '--to',
                        help='date to which search for in form of d/m/Y')
    parser.add_argument('-d', '--duration', default=90,
                        help='default event duration in minutes')
    parser.add_argument('-i', '--input', type=argparse.FileType('r'),
                        help='input icalendar file, if given only new events will be added')
    parser.add_argument('-o', '--output',
                        help='output icalendar file instead of stdout')
    #TODO parse content of pages from event URL
    #parser.add_argument('-f', '--full',
    #                    help='obtain full event description (leads to one request per event!)')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--only-SEEM', action='store_true',
                       help='search only SEEM events')
    group.add_argument('--only-regional', action='store_true',
                       help='search only regional events')
    group.add_argument('--only-national-international', action='store_true',
                       help='search only national and international events')
    return parser.parse_args()

def main():
    args = parse_args()
    global cal
    if args.input:
        cal = icalendar.Calendar.from_ical(args.input.read())
        args.input.close()
        dt_fr = datetime.datetime.strptime(args.fr, '%d/%m/%Y')
        if args.to:
            dt_to = datetime.datetime.strptime(args.to, '%d/%m/%Y')
            def keep(event):
                dt_event = datetime.datetime(*event['dtstart'].dt.timetuple()[:3])
                return dt_event < dt_fr or dt_event > dt_to
        else:
            def keep(event):
                dt_event = datetime.datetime(*event['dtstart'].dt.timetuple()[:3])
                return dt_event < dt_fr
        cal.subcomponents = [event for event in cal.subcomponents if keep(event)]
    else:
        cal = icalendar.Calendar(version=2.0,
                                 prodid='-//mahlzahn//get_cemeb_cal//EN')
    base_url = 'https://www.labex-cemeb.org'
    url = base_url + '/fr/agenda'
    if args.only_SEEM:
        what = 0
    elif args.only_regional:
        what = 1
    elif args.only_national_international:
        what = 2
    else:
        what = 'All'
    params = {
            'field_agenda_source_value': what,
            'field_agenda_date_value[value][date]': args.fr,
            'field_agenda_date_value2[value][date]': args.to,
            }
    pages = []
    with requests.Session() as s:
        r = s.get(url, params=params)
        if r.ok:
            pages.append(r.text)
        else:
            raise RuntimeError('Request was not successful')
        if m := re.search('<li class="pager-last last">.*page=(\d*)"', r.text):
            for page in range(1, int(m.groups()[0]) + 1):
                params['page'] = page
                r = s.get(url, params=params)
                if r.ok:
                    pages.append(r.text)
                else:
                    raise RuntimeError('Request was not successful')
    events = []
    for page in pages:
        events += get_events(page, base_url=base_url)
    vevents = get_vevents(events, base_url=base_url, default_duration=args.duration)
    for vevent in vevents:
        cal.add_component(vevent)
    if args.output:
        with open(args.output, 'wb') as f:
            f.write(cal.to_ical())
    else:
        print(cal.to_ical().decode())

class Event(argparse.Namespace):
    ...

def get_events(page, base_url):
    body = bs4.BeautifulSoup(page, features='lxml').body
    agenda = body.find_all(
            lambda tag: 
            tag.name == 'div'
            and tag.has_attr('class')
            and 'view-agenda' in tag['class'])[-1]
    events_raw = agenda.find_all(
            lambda tag:
            tag.name == 'div'
            and tag.has_attr('class')
            and 'views-row' in tag['class'])
    events = []
    for event_raw in events_raw:
        link = event_raw.find(
                lambda tag:
                tag.name == 'span'
                and tag.has_attr('class')
                and 'title' in tag['class']).find('a')
        url = base_url + link['href']
        title = link.contents[0]
        date = event_raw.find_all(
                lambda tag:
                tag.name == 'span'
                and tag.has_attr('class')
                and 'date-display-single' in tag['class'])[:2]
        try:
            day, month_year = date
            day = int(day.contents[0])
            month, year = month_year.contents[0].split()
            year = int(year)
            month = {'jan': 1, 'fév': 2, 'mar': 3, 'avr': 4, 'mai': 5, 'juin': 6,
                     'juil': 7, 'aoû': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'déc': 12
                     }[month]
        except:
            year = month = day = None
        location = event_raw.find(
                lambda tag:
                tag.name == 'span'
                and tag.has_attr('class')
                and 'lieu' in tag['class']).contents
        if location:
            location = location[0]
        else:
            location = ''
        if m := re.match('(\d*)h(\d*) ', location):
            hour, minute = m.groups()
            hour = int(hour)
            minute = int(minute)
            location = location[m.end():]
        else:
            hour = None
            minute = None
        abstract = event_raw.find(
                lambda tag:
                tag.name == 'span'
                and tag.has_attr('class')
                and 'resume' in tag['class']).contents
        abstract = ''.join(str(a) for a in abstract)
        try:
            image = event_raw.find(
                    lambda tag:
                    tag.name == 'div'
                    and tag.has_attr('class')
                    and 'visuel' in tag['class']).find('img')['src']
        except:
            image = None
        event = Event(
                title=title,
                url=url,
                year=year,
                day=day,
                month=month,
                hour=hour,
                minute=minute,
                location=location,
                abstract=abstract,
                image=image,
                )
        events.append(event)
    return events

def get_vevents(events, base_url, default_duration=90):
    dtstamp = datetime.datetime.utcnow().replace(microsecond=0)
    tzinfo = zoneinfo.ZoneInfo('Europe/Paris')
    vevents = []
    for i, event in enumerate(events):
        vevent = icalendar.Event()
        vevent.add('dtstamp', dtstamp)
        #TODO determined UID, but following could fail with duplicate URLs
        #vevent.add('uid', uuid.uuid3(uuid.NAMESPACE_URL, event.url))
        vevent.add('uid', uuid.uuid4())
        if event.hour is None:
            vevent.add('dtstart', datetime.date(event.year,
                                                    event.month,
                                                    event.day))
            vevent.add('dtend', vevent['dtstart'].dt + datetime.timedelta(days=1))
        else:
            vevent.add('dtstart', datetime.datetime(event.year,
                                                    event.month,
                                                    event.day,
                                                    event.hour,
                                                    event.minute,
                                                    tzinfo=tzinfo))
            vevent.add('duration', datetime.timedelta(minutes=default_duration))
        if event.image:
            vevent.add('attach', event.image, {'value': 'URI'})
        vevent.add('source', base_url, {'value': 'URI'})
        vevent.add('description', event.abstract)
        vevent.add('location', event.location)
        vevent.add('summary', event.title)
        vevent.add('url', event.url, {'value': 'URI'})
        vevents.append(vevent)
    return vevents

if __name__ == "__main__":
    main()


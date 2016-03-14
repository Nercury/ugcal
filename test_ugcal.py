from __future__ import absolute_import

import pytest
from ugcal import UGCal


@pytest.fixture
def php_meetup():
    return {
        u'status': u'upcoming', 
        u'updated': 1457875805000,
        u'group': {
            u'who': u'PHPers',
            u'name': u'Vilnius PHP Meetups',
            u'join_mode': u'open',
            u'created': 1416565027000,
            u'lon': 25.270000457763672,
            u'lat': 54.70000076293945,
            u'urlname': u'vilniusphp', 
            u'id': 18204759
        },
        u'name': u'VilniusPHP 0x29',
        u'created': 1418629034000,
        u'venue': {
            u'city': u'Vilnius',
            u'name': u'\u0160MTP',
            u'repinned': False,
            u'lon': 25.294130325317383,
            u'localized_country_name': u'Lithuania',
            u'address_1': u'J. Galvyd\u017eio g. 5, Vilnius',
            u'country': u'lt',
            u'lat': 54.710880279541016,
            u'id': 23491895
        },
        u'utc_offset': 10800000,
        u'visibility': u'public',
        u'yes_rsvp_count': 5,
        u'link': u'http://www.meetup.com/vilniusphp/events/228864161/',
        u'time': 1460043000000,
        u'duration': 9000000,
        u'waitlist_count': 0,
        u'id': u'gnbddlyvgbkb',
        u'description': u"<p>Speakers: TBA</p> <p>Do you have what to share with community? Feel free to contact us and we'll register you as a speaker!</p> "  # noqa
    }


def test_existing_events_by_links():
    php_meetup = {
        'link': 'http://www.meetup.com/php_meetup/events/123456/'
    }
    js_meetup = {
        'link': 'http://www.meetup.com/js_meetup/events/654321/'
    }

    php_event = {
        'description': 'lorem ipsum http://www.meetup.com/php_meetup/events/123456/ somehting else.'  # noqa
    }
    ruby_event = {
        'description': ''
    }

    meetups = [php_meetup, js_meetup]
    gcal_events = [php_event, ruby_event]

    result = UGCal.find_existing_events(meetups, gcal_events)
    assert {
        'http://www.meetup.com/php_meetup/events/123456/': php_event
    } == result


def test_filter_events_to_create():
    old_php_meetup = {
        'link': 'http://www.meetup.com/php_meetup/events/123456/'
    }
    new_php_meetup = {
        'link': 'http://www.meetup.com/php_meetup/events/987654/'
    }

    meetups = [old_php_meetup, new_php_meetup]
    existing = {
        'http://www.meetup.com/php_meetup/events/123456/': old_php_meetup
    }

    result = UGCal.filter_for_creation(meetups, existing)
    assert {
        'http://www.meetup.com/php_meetup/events/987654/': new_php_meetup
    } == result


def test_build_description(php_meetup):
    description = UGCal.build_description(php_meetup)

    expect = """RSVP: http://www.meetup.com/vilniusphp/events/228864161/

Speakers: TBA

Do you have what to share with community? Feel free to contact us and we'll
register you as a speaker!

"""
    result = UGCal.build_description(php_meetup)
    assert expect == result

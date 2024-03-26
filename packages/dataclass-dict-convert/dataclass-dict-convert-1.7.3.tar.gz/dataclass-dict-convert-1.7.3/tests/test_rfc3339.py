import datetime

import pytest
from datetime import timedelta
from pstats import SortKey

from dateutil.tz import tzlocal
from dateutil.parser import parse as dateutil_parse

from dataclass_dict_convert import parse_rfc3339, dump_rfc3339, datetime_now
from dataclass_dict_convert.rfc3339 import parse_rfc3339_no_none


def test_dump_rfc3339_a():
    expected = '2020-03-04T22:33:45Z'
    dt = parse_rfc3339(expected)
    actual = dump_rfc3339(dt)
    assert actual == expected


def test_dump_rfc3339_b():
    expected = '2020-03-04T22:33:45Z'
    orig = '2020-03-04T22:33:45+00:00'
    dt = parse_rfc3339(orig)
    actual = dump_rfc3339(dt)
    assert actual == expected


def test_dump_rfc3339_c():
    expected = '2020-03-04T22:33:45Z'
    orig = '2020-03-04T23:33:45+01:00'
    dt = parse_rfc3339(orig)
    actual = dump_rfc3339(dt)
    assert actual == expected


def test_dump_rfc3339_d():
    expected = '2020-03-04T22:33:45Z'
    orig = '2020-03-04T23:33:45+01:00'
    dt = parse_rfc3339(orig)
    actual = dump_rfc3339(dt, zulu=False)
    assert not actual.endswith('Z') and not actual.endswith('00:00')
    assert dump_rfc3339(parse_rfc3339(actual)) == expected


def test_dump_rfc3339_e():
    expected = '2020-03-04T23:33:45.1234Z'
    dt = parse_rfc3339(expected)
    actual = dump_rfc3339(dt, no_milliseconds=False)
    assert dt == parse_rfc3339(actual)


def test_dump_rfc3339_f():
    expected = '2020-03-04T22:33:45Z'
    orig = '2020-03-04T23:33:45.1234+01:00'
    dt = parse_rfc3339(orig)
    actual = dump_rfc3339(dt)
    assert actual == expected


def test_dump_rfc3339_naive():
    dt = datetime.datetime(2000, 1, 2, 3, 4, 5, 0)
    with pytest.raises(ValueError):
        print(dump_rfc3339(dt))


def test_now1():
    actual = datetime_now(zulu=True, no_milliseconds=True)
    assert actual.microsecond == 0
    assert dump_rfc3339(actual).endswith('Z')


def test_now2():
    actual = datetime_now(zulu=True, no_milliseconds=False)
    assert actual.microsecond != 0  # very small chance it is 0, which will make this test fail...
    assert dump_rfc3339(actual).endswith('Z')


def test_now3():
    actual = datetime_now(zulu=False, no_milliseconds=True)
    print('local timezone offset = {}'.format(tzlocal()._std_offset))
    if tzlocal()._std_offset == 0 or tzlocal()._dst_offset == 0:
        return  # cannot test when local timezone is UTC or near it
    assert actual.microsecond == 0
    actual_str = dump_rfc3339(actual, zulu=False, no_milliseconds=False)
    print('actual_str = {}'.format(actual_str))
    assert not actual_str.endswith('Z') and not actual_str.endswith('00:00')


def parser_test_helper(a_date_str: str):
    # This tests assumes dump_rfc3339 and dateutil.parser.parse() are 100% correct
    parsed_date1 = parse_rfc3339(a_date_str)
    parsed_date2 = dateutil_parse(a_date_str)
    assert parsed_date1 == parsed_date2, \
        'actual {} != expected {} for {}'.format(parsed_date1, parsed_date2, a_date_str)
    restored_text = dump_rfc3339(parsed_date1, zulu=False, no_milliseconds=False)
    restored_date = dateutil_parse(restored_text)
    assert restored_date == parsed_date1, \
        '2nd compare failed: restored_date={} parsed_date1={} in={}'.format(restored_date, parsed_date1, a_date_str)


def test_parse_rfc3339_a():
    parser_test_helper('2020-03-04T22:33:45Z')


def test_parse_rfc3339_b1():
    parser_test_helper('2020-03-04T22:33:45.123456Z')


def test_parse_rfc3339_b2():
    parser_test_helper('2020-03-04T22:33:45.1Z')


def test_parse_rfc3339_b3():
    parser_test_helper('2020-03-04T22:33:45.0012Z')


def test_parse_rfc3339_c():
    parser_test_helper('2020-03-04T22:33:45+04:00')


def test_parse_rfc3339_d():
    parser_test_helper('2020-03-04T22:33:45-04:00')


def test_parse_rfc3339_e():
    parser_test_helper('2020-03-04T22:33:45-00:00')


def test_parse_rfc3339_f():
    parser_test_helper('2020-03-04T22:33:45+00:00')


def test_parse_rfc3339_g():
    parser_test_helper('2020-03-04T22:33:45.123456+04:00')


def test_parse_rfc3339_h():
    parser_test_helper('2020-03-04T22:33:45.123456-04:00')


def test_parse_rfc3339_i():
    parser_test_helper('2020-03-04T22:33:45.123456+00:00')


def test_parse_rfc3339_j():
    parser_test_helper('2020-03-04T22:33:45.123456-00:00')


def test_parse_rfc3339_none_a():
    parsed_date = parse_rfc3339(None)
    assert parsed_date is None


def test_parse_rfc3339_none_b():
    with pytest.raises(ValueError):
        parsed_date = parse_rfc3339_no_none(None)
        print(parsed_date)


def test_parse_rfc3339_no_tz_a():
    parsed_date = parse_rfc3339('2020-03-04T22:33:45', none_if_empty_tz=True)
    assert parsed_date is None


def test_parse_rfc3339_no_tz_b():
    with pytest.raises(ValueError):
        parsed_date = parse_rfc3339('2020-03-04T22:33:45')
        print(parsed_date)


def test_parse_rfc3339_no_tz_c():
    with pytest.raises(ValueError):
        parsed_date = parse_rfc3339_no_none('2020-03-04T22:33:45')
        print(parsed_date)


PERFORMANCE_TEST_SIZE = 10000


def test_performance_parse_rfc3339():
    start = datetime.datetime.now(datetime.timezone.utc)
    tested_date_strs = ['2020-03-04T23:33:45.1234+01:00', '2020-03-04T23:33:45.123456-08:00',
                        '2020-03-04T23:33:45+01:00', '2020-03-04T23:33:45.1234Z',
                        '2020-03-04T23:33:45+01:00']
    import cProfile
    with cProfile.Profile() as pr:
        for i in range(1, PERFORMANCE_TEST_SIZE):
            parse_rfc3339(tested_date_strs[i % len(tested_date_strs)])
    # pr.print_stats(sort=SortKey.TIME)
    pr.print_stats(sort=SortKey.CUMULATIVE)
    end = datetime.datetime.now(datetime.timezone.utc)
    diff: timedelta = end - start
    print('parse_rfc3339() performance: {} s for {}'.format(diff.total_seconds(), PERFORMANCE_TEST_SIZE))
    assert diff.total_seconds() < 1.0, 'bad parse_rfc3339() performance: {} s for {}'\
        .format(diff.total_seconds(), PERFORMANCE_TEST_SIZE)

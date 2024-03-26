import datetime

import pytest
from dataclasses import dataclass
from stringcase import camelcase
from typing import Optional, List, Dict, Union, Any

from dataclass_dict_convert import dataclass_dict_convert, dataclass_copy_method, dataclass_auto_type_check
from dataclass_dict_convert.dataclass_utils import dataclass_fields_type_check, dataclass_multiline_repr


def test_dataclass_fields_type_check1():
    @dataclass
    class T:
        a: int
    t = T(1)
    dataclass_fields_type_check(t)


def test_dataclass_fields_type_check2():
    @dataclass
    class T:
        a: int
    t = T('blah')
    with pytest.raises(TypeError):
        dataclass_fields_type_check(t)


def test_dataclass_fields_type_check3():
    @dataclass
    class T:
        a: Optional[int]
    t = T('blah')
    with pytest.raises(TypeError):
        dataclass_fields_type_check(t)


def test_dataclass_fields_type_check4():
    @dataclass
    class T:
        a: Optional[int]
    t = T(5)
    dataclass_fields_type_check(t)


def test_dataclass_fields_type_check5():
    @dataclass
    class T:
        a: Optional[int]
    t = T(None)
    dataclass_fields_type_check(t)


def test_dataclass_fields_type_check6():
    @dataclass
    class T:
        a: List[str]
    t = T(['foo', 'bar'])
    dataclass_fields_type_check(t)


def test_dataclass_fields_type_check7():
    @dataclass
    class T:
        a: List[str]
    t = T([])
    dataclass_fields_type_check(t)


def test_dataclass_fields_type_check8():
    @dataclass
    class T:
        a: List[str]
    t = T(['foo', 1])
    with pytest.raises(TypeError):
        dataclass_fields_type_check(t)


def test_dataclass_fields_type_check9():
    @dataclass
    class T:
        a: List[str]
    t = T([1])
    with pytest.raises(TypeError):
        dataclass_fields_type_check(t)


def test_dataclass_fields_type_check10():
    @dataclass
    class T:
        a: List[str]
    t = T(None)
    with pytest.raises(TypeError):
        dataclass_fields_type_check(t)


def test_dataclass_fields_type_check11():
    @dataclass
    class T:
        a: List[str]
    t = T('foobar')
    with pytest.raises(TypeError):
        dataclass_fields_type_check(t)


def test_dataclass_fields_type_check12():
    @dataclass
    class T:
        a: Union[str, int]
    t = T('foobar')
    dataclass_fields_type_check(t)


def test_dataclass_fields_type_check13():
    @dataclass
    class T:
        a: Union[str, int]
    t = T(1)
    dataclass_fields_type_check(t)


def test_dataclass_fields_type_check14():
    @dataclass
    class T:
        a: Union[str, int]
    t = T(None)
    with pytest.raises(TypeError):
        dataclass_fields_type_check(t)


def test_dataclass_fields_type_check15():
    @dataclass
    class T:
        a: Union[str, int]
    t = T(0.5)
    with pytest.raises(TypeError):
        dataclass_fields_type_check(t)


def test_dataclass_fields_type_check16():
    @dataclass
    class X:
        x: str

    @dataclass
    class T:
        a: X
    t = T(X('foo'))
    dataclass_fields_type_check(t)


def test_dataclass_fields_type_check17():
    @dataclass
    class X:
        x: str

    @dataclass
    class Y:
        y: str

    @dataclass
    class T:
        a: X
    t = T(Y(1234))
    with pytest.raises(TypeError):
        dataclass_fields_type_check(t)


def test_dataclass_fields_type_check18():
    @dataclass
    class X:
        x: str

    @dataclass
    class T:
        a: X
    t = T('blah')
    with pytest.raises(TypeError):
        dataclass_fields_type_check(t)


def test_dataclass_fields_type_check19():
    @dataclass
    class X:
        x: str

    @dataclass
    class T:
        a: X
    t = T(X(1234)) # no problem as only a is checked
    dataclass_fields_type_check(t)


def test_dataclass_fields_type_check20():
    @dataclass
    class X:
        x: str

    @dataclass
    class T:
        a: Optional[X]
    t = T(X('foo'))
    dataclass_fields_type_check(t)


def test_dataclass_fields_type_check21():
    @dataclass
    class X:
        x: str

    @dataclass
    class T:
        a: Optional[X]
    t = T(None)
    dataclass_fields_type_check(t)


NAIVE_DATE = datetime.datetime.now(None)
NON_NAIVE_DATE = datetime.datetime.now(datetime.timezone.utc)
assert NAIVE_DATE.tzinfo is None
assert NON_NAIVE_DATE.tzinfo is not None


def test_dataclass_fields_type_check_datetime1():
    @dataclass
    class T:
        a: datetime.datetime
    t = T(NON_NAIVE_DATE)
    dataclass_fields_type_check(t)


def test_dataclass_fields_type_check_datetime2():
    @dataclass
    class T:
        a: datetime.datetime
    t = T(NAIVE_DATE)
    with pytest.raises(TypeError):
        dataclass_fields_type_check(t)


def test_dataclass_fields_type_check_datetime3():
    @dataclass
    class T:
        a: datetime.datetime
    t = T('20190102T01:20:34Z')
    with pytest.raises(TypeError):
        dataclass_fields_type_check(t)



def test_dataclass_fields_type_check_optdatetime1():
    @dataclass
    class T:
        a: Optional[datetime.datetime]
    t = T(NON_NAIVE_DATE)
    dataclass_fields_type_check(t)


def test_dataclass_fields_type_check_optdatetime2():
    @dataclass
    class T:
        a: Optional[datetime.datetime]
    t = T(NAIVE_DATE)
    with pytest.raises(TypeError):
        dataclass_fields_type_check(t)


def test_dataclass_fields_type_check_optdatetime3():
    @dataclass
    class T:
        a: Optional[datetime.datetime]
    t = T(None)
    dataclass_fields_type_check(t)


def test_dataclass_copy_method_decorator1():
    @dataclass_copy_method
    @dataclass_dict_convert(dict_letter_case=camelcase)
    @dataclass
    class T:
        a: int
    t = T(1)
    tt = t.make_copy()
    assert t == tt


def test_dataclass_copy_method_decorator2():
    @dataclass_copy_method
    @dataclass_dict_convert(dict_letter_case=camelcase)
    @dataclass
    class T:
        a: int
        b: str
        c: List[str]
    t = T(1, 'foo', ['bar', 'baz'])
    tt = t.make_copy()
    assert t == tt


def test_dataclass_copy_method_decorator3():
    @dataclass_dict_convert(dict_letter_case=camelcase)
    @dataclass
    class X:
        x: float

    @dataclass_copy_method
    @dataclass_dict_convert(dict_letter_case=camelcase)
    @dataclass
    class T:
        a: X
        b: str
        c: List[str]
    t = T(X(0.5), 'foo', ['bar', 'baz'])
    tt = t.make_copy()
    assert isinstance(tt.a, X)
    assert tt.a.x == 0.5
    assert t == tt


def test_dataclass_copy_method_decorator1rev():
    @dataclass_dict_convert(dict_letter_case=camelcase)
    @dataclass
    @dataclass_copy_method
    class T:
        a: int
    t = T(1)
    tt = t.make_copy()
    assert t == tt


def test_dataclass_copy_method_decorator2rev():
    @dataclass_dict_convert(dict_letter_case=camelcase)
    @dataclass
    @dataclass_copy_method
    class T:
        a: int
        b: str
        c: List[str]
    t = T(1, 'foo', ['bar', 'baz'])
    tt = t.make_copy()
    assert t == tt


def test_dataclass_copy_method_decorator3rev():
    @dataclass_dict_convert(dict_letter_case=camelcase)
    @dataclass
    class X:
        x: float

    @dataclass_dict_convert(dict_letter_case=camelcase)
    @dataclass
    @dataclass_copy_method
    class T:
        a: X
        b: str
        c: List[str]
    t = T(X(0.5), 'foo', ['bar', 'baz'])
    tt = t.make_copy()
    assert isinstance(tt.a, X)
    # assert tt.a.x == 0.5
    # assert tt.b == 'foo'
    assert t == tt


def test_dataclass_auto_type_check_decorator1():
    @dataclass
    @dataclass_auto_type_check
    class T:
        a: int
    t = T(1)
    dataclass_fields_type_check(t)


def test_dataclass_auto_type_check_decorator2a():
    @dataclass
    @dataclass_auto_type_check
    class T:
        a: int
    with pytest.raises(TypeError):
        t = T('blah')
        print('t.a={}'.format(t.a))


def test_dataclass_auto_type_check_decorator2b():
    @dataclass
    @dataclass_auto_type_check
    class T:
        a: int
        def __post_init__(self):
            print('2b T.__post_init__ a={}'.format(self.a))
    with pytest.raises(TypeError):
        t = T('blah')
        print('t.a={}'.format(t.a))


def test_dataclass_auto_type_check_decorator3():
    @dataclass
    @dataclass_auto_type_check
    class T:
        a: Optional[int]
    with pytest.raises(TypeError):
        t = T('blah')


def test_dataclass_auto_type_check_decorator4():
    @dataclass
    @dataclass_auto_type_check
    class T:
        a: Optional[int]
    t = T(5)
    dataclass_fields_type_check(t)


def test_dataclass_auto_type_check_decorator5():
    @dataclass
    @dataclass_auto_type_check
    class T:
        a: Optional[int]
    t = T(None)
    dataclass_fields_type_check(t)


def test_dataclass_auto_type_check_decorator6():
    @dataclass
    @dataclass_auto_type_check
    class T:
        a: List[str]
    t = T(['foo', 'bar'])
    dataclass_fields_type_check(t)


def test_dataclass_auto_type_check_decorator7():
    @dataclass
    @dataclass_auto_type_check
    class T:
        a: List[str]
    t = T([])
    dataclass_fields_type_check(t)


def test_dataclass_auto_type_check_decorator8():
    @dataclass
    @dataclass_auto_type_check
    class T:
        a: List[str]
    with pytest.raises(TypeError):
        t = T(['foo', 1])


def test_dataclass_auto_type_check_decorator9():
    @dataclass
    @dataclass_auto_type_check
    class T:
        a: List[str]
    with pytest.raises(TypeError):
        t = T([1])


def test_dataclass_auto_type_check_decorator10():
    @dataclass
    @dataclass_auto_type_check
    class T:
        a: List[str]
    with pytest.raises(TypeError):
        t = T(None)


def test_dataclass_auto_type_check_decorator11():
    @dataclass
    @dataclass_auto_type_check
    class T:
        a: List[str]
    with pytest.raises(TypeError):
        t = T('foobar')


def test_dataclass_auto_type_check_decorator12():
    @dataclass
    @dataclass_auto_type_check
    class T:
        a: Union[str, int]
    t = T('foobar')
    dataclass_fields_type_check(t)


def test_dataclass_auto_type_check_decorator13():
    @dataclass
    @dataclass_auto_type_check
    class T:
        a: Union[str, int]
    t = T(1)
    dataclass_fields_type_check(t)


def test_dataclass_auto_type_check_decorator14():
    @dataclass
    @dataclass_auto_type_check
    class T:
        a: Union[str, int]
    with pytest.raises(TypeError):
        t = T(None)


def test_dataclass_auto_type_check_decorator15():
    @dataclass
    @dataclass_auto_type_check
    class T:
        a: Union[str, int]
    with pytest.raises(TypeError):
        t = T(0.5)


def test_dataclass_auto_type_check_decorator16():
    @dataclass
    class X:
        x: str

    @dataclass
    @dataclass_auto_type_check
    class T:
        a: X
    t = T(X('foo'))
    dataclass_fields_type_check(t)


def test_dataclass_auto_type_check_decorator17():
    @dataclass
    class X:
        x: str

    @dataclass
    class Y:
        y: str

    @dataclass
    @dataclass_auto_type_check
    class T:
        a: X
    with pytest.raises(TypeError):
        t = T(Y(1234))


def test_dataclass_auto_type_check_decorator18():
    @dataclass
    class X:
        x: str

    @dataclass
    @dataclass_auto_type_check
    class T:
        a: X
    with pytest.raises(TypeError):
        t = T('blah')


def test_dataclass_auto_type_check_decorator19():
    @dataclass
    class X:
        x: str

    @dataclass
    @dataclass_auto_type_check
    class T:
        a: X
    t = T(X(1234)) # no problem as only a is checked
    dataclass_fields_type_check(t)


def test_dataclass_auto_type_check_decorator20():
    @dataclass
    class X:
        x: str

    @dataclass
    @dataclass_auto_type_check
    class T:
        a: Optional[X]
    t = T(X('foo'))
    dataclass_fields_type_check(t)


def test_dataclass_auto_type_check_decorator21():
    @dataclass
    class X:
        x: str

    @dataclass
    @dataclass_auto_type_check
    class T:
        a: Optional[X]
    t = T(None)
    dataclass_fields_type_check(t)


NAIVE_DATE = datetime.datetime.now(None)
NON_NAIVE_DATE = datetime.datetime.now(datetime.timezone.utc)


def test_dataclass_auto_type_check_decorator_datetime1():
    @dataclass
    @dataclass_auto_type_check
    class T:
        a: datetime.datetime
    t = T(NON_NAIVE_DATE)


def test_dataclass_auto_type_check_decorator_datetime2():
    @dataclass
    @dataclass_auto_type_check
    class T:
        a: datetime.datetime
    with pytest.raises(TypeError):
        t = T(NAIVE_DATE)


def test_dataclass_auto_type_check_decorator_datetime3():
    @dataclass
    @dataclass_auto_type_check
    class T:
        a: datetime.datetime
    with pytest.raises(TypeError):
        t = T('20190102T01:20:34Z')



def test_dataclass_auto_type_check_decorator_optdatetime1():
    @dataclass
    @dataclass_auto_type_check
    class T:
        a: Optional[datetime.datetime]
    t = T(NON_NAIVE_DATE)
    dataclass_fields_type_check(t)


def test_dataclass_auto_type_check_decorator_optdatetime2():
    @dataclass
    @dataclass_auto_type_check
    class T:
        a: Optional[datetime.datetime]
    with pytest.raises(TypeError):
        t = T(NAIVE_DATE)


def test_dataclass_auto_type_check_decorator_dict1():
    @dataclass
    @dataclass_auto_type_check
    class T:
        a: Dict[str, int]
    with pytest.raises(TypeError):
        t = T({'a': 'b'})


def test_dataclass_auto_type_check_decorator_dict2():
    @dataclass
    @dataclass_auto_type_check
    class T:
        a: Dict[str, int]
    with pytest.raises(TypeError):
        t = T({'a': 1, 'b': 'c', 'c': 3})


def test_dataclass_auto_type_check_decorator_dict3():
    @dataclass
    @dataclass_auto_type_check
    class T:
        a: Dict[str, int]
    t = T({'a': 1, 'b': 2, 'c': 3})


def test_dataclass_auto_type_check_decorator_dict4():
    @dataclass
    @dataclass_auto_type_check
    class T:
        a: Dict[str, int]
    t = T({'a': 1, 'b': 2, 'c': 3})


def test_dataclass_auto_type_check_decorator_dict6():
    @dataclass
    @dataclass_auto_type_check
    class U:
        b: int

    @dataclass
    @dataclass_auto_type_check
    class T:
        a: Dict[str, U]
    t = T({'a': U(1), 'b': U(2), 'c': U(3)})


def test_dataclass_auto_type_check_decorator_dict7():
    @dataclass
    @dataclass_auto_type_check
    class U:
        b: int

    @dataclass
    @dataclass_auto_type_check
    class T:
        a: Dict[str, U]
    with pytest.raises(TypeError):
        t = T({'a': U(1), 'b': U(2), 'c': 3})


def test_dataclass_auto_type_check_decorator_dict8():
    @dataclass
    @dataclass_auto_type_check
    class T:
        a: Dict[int, int]
    t = T({1: 2, 3: 4})
    with pytest.raises(TypeError):
        t = T({1: 2, 'a': 3})


def test_dataclass_auto_type_check_decorator_dict9():
    @dataclass
    @dataclass_auto_type_check
    class T:
        a: Dict[Any, Any]
    t = T({1: 2, 3: 4})
    t = T({1: '2', 'a': 3})


def test_dataclass_auto_type_check_decorator_dict10():
    @dataclass
    @dataclass_auto_type_check
    class T:
        a: Dict[int, List[int]]
    t = T({1: [2, 3], 4: [5, 6]})
    t = T({1: [2, 3], 4: []})
    with pytest.raises(TypeError):
        t = T({1: ['a'], 4: [5, 6]})
    with pytest.raises(TypeError):
        t = T({1: [2, 3], 4: [5, 'a']})
    with pytest.raises(TypeError):
        t = T({'a': [2, 3], 4: [5, 6]})


def test_dataclass_auto_type_check_decorator_opt_dict0():
    @dataclass
    @dataclass_auto_type_check
    class T:
        a: Optional[Dict[str, int]]
    t = T(None)

def test_dataclass_auto_type_check_decorator_opt_dict1():
    @dataclass
    @dataclass_auto_type_check
    class T:
        a: Optional[Dict[str, int]]
    with pytest.raises(TypeError):
        t = T({'a': 'b'})
    with pytest.raises(TypeError):
        t = T(['a', 'b'])
    with pytest.raises(TypeError):
        t = T(('a', 'b'))
    with pytest.raises(TypeError):
        t = T('a')


def test_dataclass_auto_type_check_decorator_opt_dict2():
    @dataclass
    @dataclass_auto_type_check
    class T:
        a: Optional[Dict[str, int]]
    with pytest.raises(TypeError):
        t = T({'a': 1, 'b': 'c', 'c': 3})


def test_dataclass_auto_type_check_decorator_opt_dict3():
    @dataclass
    @dataclass_auto_type_check
    class T:
        a: Optional[Dict[str, int]]
    t = T({'a': 1, 'b': 2, 'c': 3})


def test_dataclass_auto_type_check_decorator_opt_dict4():
    @dataclass
    @dataclass_auto_type_check
    class T:
        a: Optional[Dict[str, int]]
    t = T({'a': 1, 'b': 2, 'c': 3})


def test_dataclass_auto_type_check_decorator_opt_dict6():
    @dataclass
    @dataclass_auto_type_check
    class U:
        b: int

    @dataclass
    @dataclass_auto_type_check
    class T:
        a: Optional[Dict[str, U]]
    t = T({'a': U(1), 'b': U(2), 'c': U(3)})


def test_dataclass_auto_type_check_decorator_opt_dict7():
    @dataclass
    @dataclass_auto_type_check
    class U:
        b: int

    @dataclass
    @dataclass_auto_type_check
    class T:
        a: Optional[Dict[str, U]]
    with pytest.raises(TypeError):
        t = T({'a': U(1), 'b': U(2), 'c': 3})


def test_dataclass_auto_type_check_decorator_opt_dict8():
    @dataclass
    @dataclass_auto_type_check
    class T:
        a: Optional[Dict[int, int]]
    t = T({1: 2, 3: 4})
    with pytest.raises(TypeError):
        t = T({1: 2, 'a': 3})


def test_dataclass_auto_type_check_decorator_opt_dict9():
    @dataclass
    @dataclass_auto_type_check
    class T:
        a: Optional[Dict]
    t = T(None)


def test_dataclass_auto_type_check_decorator_opt_dict10():
    @dataclass
    @dataclass_auto_type_check
    class T:
        a: Optional[Dict]
    t = T({1: 2, 'a': 'b'})
    with pytest.raises(TypeError):
        t = T(['a', 'b'])


def test_dataclass_auto_type_check_decorator_opt_dict11():
    @dataclass
    @dataclass_auto_type_check
    class T:
        a: Optional[Dict[Any, Any]]
    t = T({1: 2, 3: 4})
    t = T({1: '2', 'a': 3})


def test_dataclass_auto_type_check_decorator_opt_dict12():
    @dataclass
    @dataclass_auto_type_check
    class T:
        a: Optional[Dict[str, List[str]]]
    t = T({'1': ['2', '3'], '4': ['5', '6']})
    t = T({'1': ['2', '3'], '4': []})
    t = T(None)
    with pytest.raises(TypeError):
        t = T({'1': ['2', '3'], '4': ['5', 6]})
    with pytest.raises(TypeError):
        t = T({1: ['2', '3'], '4': ['5', '6']})


def test_bug_1():
    # A bug that was encountered. Caused by Any type. (tests for Any also added)

    @dataclass_dict_convert(dict_letter_case=camelcase)
    @dataclass(frozen=True)
    @dataclass_auto_type_check
    @dataclass_copy_method
    @dataclass_multiline_repr
    class RspecSite:
        public_data: Optional[Dict[str, Any]]

    t = RspecSite(None)
    t = RspecSite({})
    t = RspecSite({'public_data': None})
    t = RspecSite({'public_data': {'a': 1, 'b': 'c'}})


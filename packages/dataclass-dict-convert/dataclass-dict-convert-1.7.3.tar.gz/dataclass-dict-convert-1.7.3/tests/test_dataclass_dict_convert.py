import dataclasses
import json
from abc import ABC
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List, Optional, Union, Dict, Any

import pytest
from stringcase import camelcase, snakecase

from dataclass_dict_convert import dataclass_dict_convert, create_wrap_in_list_from_convertor, \
    create_dict_of_dataclasses_to_convertor, create_dict_of_dataclasses_from_convertor, datetime_now, parse_rfc3339, \
    dataclass_multiline_repr
from dataclass_dict_convert.convert import _is_optional, SimpleTypeConvertor, TypeConvertorError, UnknownFieldError


def test_dataclass_dict_convert_1():
    @dataclass_dict_convert(
        dict_letter_case=camelcase
    )
    @dataclass(frozen=True)
    class Test:
        an_int: int
        a_str: str
        a_float: float
        a_bool: bool

    the_instance = Test(1, 'foo', 0.1, True)
    the_dict = {
        'anInt': 1,
        'aStr': 'foo',
        'aFloat': 0.1,
        'aBool': True,
    }

    assert 'anInt' == camelcase('an_int')

    expected = the_dict
    actual = the_instance.to_dict()
    assert actual == expected

    expected = the_instance
    actual = Test.from_dict(the_dict)
    assert actual == expected


def test_dataclass_dict_convert_2():
    @dataclass_dict_convert(
        dict_letter_case=camelcase
    )
    @dataclass(frozen=True)
    class Test:
        a_list: List[int]
        b_list: List[int]

    the_instance = Test([1, 2, 3], [])
    the_dict = {
        'aList': [1, 2, 3],
        'bList': [],
    }

    expected = the_dict
    actual = the_instance.to_dict()
    assert actual == expected

    expected = the_instance
    actual = Test.from_dict(the_dict)
    assert actual == expected


def test_is_optional_1():
    @dataclass
    class Test:
        an_opt1: Optional[int]
        an_opt2: Union[None, int]
        an_opt3: Union[int, None]
        an_opt4: Union[Optional[int], int]
        an_opt5: Union[List[int], None]
        an_opt6: Union[None, List[int]]

    for field in dataclasses.fields(Test):
        assert _is_optional(field.type)


def test_is_optional_2():
    @dataclass
    class Test:
        an_opt1: int
        an_opt2: Union[str, int]
        an_opt3: Union[List[int], int]
        an_opt4: Union[List[str], List[int]]

    for field in dataclasses.fields(Test):
        assert not _is_optional(field.type)


def test_dataclass_dict_convert_3():
    @dataclass_dict_convert(
        dict_letter_case=camelcase
    )
    @dataclass(frozen=True)
    class Test:
        an_opt: Optional[int]
        an_opt2: Optional[int]

    the_instance = Test(42, None)
    the_dict = {
        'anOpt': 42,
        'anOpt2': None,
    }

    expected = the_dict
    actual = the_instance.to_dict()
    assert actual == expected

    expected = the_instance
    actual = Test.from_dict(the_dict)
    assert actual == expected


def test_dataclass_dict_convert_composition_4():
    @dataclass_dict_convert(
        dict_letter_case=camelcase
    )
    @dataclass(frozen=True)
    class TestB:
        an_int: int
        a_str: str
        a_float: float
        a_bool: bool

    @dataclass_dict_convert(
        dict_letter_case=camelcase
    )
    @dataclass(frozen=True)
    class Test:
        nestedClass: TestB
        nestedInOpt: Optional[TestB]
        nestedInList: List[TestB]

    the_instanceB1 = TestB(1, 'foo', 0.1, True)
    the_instanceB2 = TestB(2, 'bar', 0.2, False)
    the_instanceB3 = TestB(3, 'baz', 0.3, True)
    the_instanceB4 = TestB(4, 'huh', 0.4, False)
    the_instance = Test(the_instanceB1, the_instanceB2, [the_instanceB3, the_instanceB4])
    the_dict = {
        'nestedClass': {'anInt': 1, 'aStr': 'foo', 'aFloat': 0.1, 'aBool': True,},
        'nestedInOpt': {'anInt': 2, 'aStr': 'bar', 'aFloat': 0.2, 'aBool': False,},
        'nestedInList': [
            {'anInt': 3, 'aStr': 'baz', 'aFloat': 0.3, 'aBool': True, },
            {'anInt': 4, 'aStr': 'huh', 'aFloat': 0.4, 'aBool': False, },
        ],
    }

    expected = the_dict
    actual = the_instance.to_dict()
    assert actual == expected

    expected = the_instance
    actual = Test.from_dict(the_dict)
    assert actual == expected


def test_dataclass_dict_convert_5fail():
    @dataclass_dict_convert(
        dict_letter_case=camelcase
    )
    @dataclass(frozen=True)
    class Test:
        a_list: List[int]
        b_list: List[str]

    the_instance = Test([1], ['ahah'])
    in_dict = {
        'aList': 1,
        'bList': 'ahah',
    }
    out_dict = {
        'aList': [1],
        'bList': ['ahah'],
    }

    expected = out_dict
    actual = the_instance.to_dict()
    assert actual == expected

    expected = the_instance
    with pytest.raises(TypeConvertorError):
        actual = Test.from_dict(in_dict)
        assert actual == expected


def test_dataclass_dict_convert_5():
    @dataclass_dict_convert(
        dict_letter_case=camelcase,
        custom_from_dict_convertors={
            'a_list': create_wrap_in_list_from_convertor(int),
            'b_list': create_wrap_in_list_from_convertor(str),
        }
    )
    @dataclass(frozen=True)
    class Test:
        a_list: List[int]
        b_list: List[str]

    the_instance = Test([1], ['ahah'])
    in_dict = {
        'aList': 1,
        'bList': 'ahah',
    }
    out_dict = {
        'aList': [1],
        'bList': ['ahah'],
    }

    expected = out_dict
    actual = the_instance.to_dict()
    assert actual == expected

    expected = the_instance
    actual = Test.from_dict(in_dict)
    assert actual == expected


def test_dataclass_dict_convert_6():
    class MyEnum(Enum):
        TESTA = 'Test A'
        TESTB = 'Test B'

    @dataclass_dict_convert(
        dict_letter_case=camelcase
    )
    @dataclass(frozen=True)
    class Test:
        an_enum: MyEnum
        an_opt_enum1: Optional[MyEnum]
        an_opt_enum2: Optional[MyEnum]

    the_instance = Test(MyEnum.TESTA, MyEnum.TESTB, None)
    the_dict = {
        'anEnum': 'TESTA',
        'anOptEnum1': 'TESTB',
        'anOptEnum2': None,
    }

    expected = the_dict
    actual = the_instance.to_dict()
    assert actual == expected

    expected = the_instance
    actual = Test.from_dict(the_dict)
    assert actual == expected


def test_dataclass_dict_convert_none_1():
    class MyEnum(Enum):
        TESTA = 'Test A'
        TESTB = 'Test B'

    @dataclass_dict_convert(
        dict_letter_case=camelcase
    )
    @dataclass(frozen=True)
    class Test:
        an_enum: MyEnum
        an_opt_enum1: Optional[MyEnum]
        an_opt_enum2: Optional[MyEnum]
        an_opt_int1: Optional[int]
        an_opt_int2: Optional[int]
        an_opt_list1: Optional[List[int]]
        an_opt_list2: Optional[List[int]]

    the_instance = Test(MyEnum.TESTA, MyEnum.TESTB, None,
                        0, None, [], None)
    the_dict = {
        'anEnum': 'TESTA',
        'anOptEnum1': 'TESTB',
        'anOptEnum2': None,
        'anOptInt1': 0,
        'anOptInt2': None,
        'anOptList1': [],
        'anOptList2': None,
    }
    the_dict_no_none = {
        'anEnum': 'TESTA',
        'anOptEnum1': 'TESTB',
        'anOptInt1': 0,
        'anOptList1': [],
    }

    expected = the_dict
    actual = the_instance.to_dict(remove_none=False)
    assert actual == expected

    expected = the_dict_no_none
    actual = the_instance.to_dict(remove_none=True)
    assert actual == expected

    expected = the_instance
    actual = Test.from_dict(the_dict)
    assert actual == expected


def test_dataclass_dict_convert_multi_1():
    @dataclass_dict_convert(
        dict_letter_case=camelcase
    )
    @dataclass(frozen=True)
    class Test:
        an_int: int
        a_str: str
        a_float: float
        a_bool: bool

    multi_instance = [Test(1, 'foo', 0.1, True), Test(2, 'bar', 0.2, False), Test(3, 'baz', 0.3, True)]
    multi_dict = [
        {'anInt': 1, 'aStr': 'foo', 'aFloat': 0.1, 'aBool': True,},
        {'anInt': 2, 'aStr': 'bar', 'aFloat': 0.2, 'aBool': False,},
        {'anInt': 3, 'aStr': 'baz', 'aFloat': 0.3, 'aBool': True,},
    ]

    expected = multi_dict
    actual = Test.to_dict_list(multi_instance)
    assert actual == expected

    expected = multi_instance
    actual = Test.from_dict_list(multi_dict)
    assert actual == expected


def test_dataclass_dict_convert_json_1():
    @dataclass_dict_convert(
        dict_letter_case=camelcase
    )
    @dataclass(frozen=True)
    class Test:
        an_int: int
        a_str: str
        a_float: float
        a_bool: bool

    the_instance = Test(1, 'foo', 0.1, True)
    the_json = """{ "anInt": 1, "aStr": "foo", "aFloat": 0.1, "aBool": true }"""

    expected = json.loads(the_json)
    actual = json.loads(the_instance.to_json())
    assert actual == expected

    expected = the_instance
    actual = Test.from_json(the_json)
    assert actual == expected



def test_dataclass_dict_convert_7():
    @dataclass_dict_convert(dict_letter_case=camelcase)
    @dataclass(frozen=True)
    class TesterB:
        an_int: int

    @dataclass_dict_convert(
        dict_letter_case=camelcase,
        custom_from_dict_convertors={
            'dict_of_tester_b': create_dict_of_dataclasses_from_convertor(TesterB, 'dict_of_tester_b')
        },
        custom_to_dict_convertors={
            'dict_of_tester_b': create_dict_of_dataclasses_to_convertor('dict_of_tester_b')
        })
    @dataclass(frozen=True)
    class TesterA:
        dict_of_tester_b: Dict[str, TesterB]

    the_instance = TesterA(dict_of_tester_b={
        'b1': TesterB(5),
        'b2': TesterB(6)
    })
    the_json = """{ "dictOfTesterB": { "b1": { "anInt": 5 }, "b2": { "anInt": 6 } } }"""

    expected = json.loads(the_json)
    actual = json.loads(the_instance.to_json())
    assert actual == expected

    expected = the_instance
    actual = TesterA.from_json(the_json)
    assert actual == expected


def test_dataclass_dict_convert_nested_dict_8():
    @dataclass_dict_convert(
        dict_letter_case=camelcase
    )
    @dataclass(frozen=True)
    class Test:
        a: Dict
        b: Optional[Dict]
        c: Optional[Dict]

    the_instance = Test({'foo': 'bar', 'baz': 1}, {'fooB': 'barB', 'bazB': 2}, None)
    the_dict = {
        'a': {'foo': 'bar', 'baz': 1},
        'b': {'fooB': 'barB', 'bazB': 2},
        'c': None
    }

    expected = the_dict
    actual = the_instance.to_dict()
    assert actual == expected

    expected = the_instance
    actual = Test.from_dict(the_dict)
    assert actual == expected


def test_dataclass_dict_convert_datetime_1():
    test_date_1_str = '2020-01-01T11:22:33Z'
    test_date_1 = parse_rfc3339(test_date_1_str)
    test_date_2_str = '2020-03-04T00:33:44Z'
    test_date_2 = parse_rfc3339(test_date_2_str)
    test_date_3_str = '2020-05-06T00:55:06Z'
    test_date_3 = parse_rfc3339(test_date_3_str)

    @dataclass_dict_convert(dict_letter_case=camelcase)
    @dataclass(frozen=True)
    class Test:
        a_date: datetime
        an_opt: Optional[datetime]
        a_list: List[datetime]
        a_dict: Dict[str, datetime]

    the_instance = Test(test_date_1, test_date_2, [test_date_3], {'key': test_date_1})
    the_dict = {
        'aDate': test_date_1_str,
        'anOpt': test_date_2_str,
        'aList': [test_date_3_str],
        'aDict': {'key': test_date_1_str},
    }

    expected = the_dict
    actual = the_instance.to_dict()
    assert actual == expected

    expected = the_instance
    actual = Test.from_dict(the_dict)
    assert actual == expected


def test_dataclass_dict_custom_class_convert_1():
    class Custom:
        def __init__(self, c: str):
            self.c = c

        def __eq__(self, other: object) -> bool:
            if isinstance(other, Custom):
                return self.c == other.c
            return NotImplemented

    test_c_1_str = 'abcdef'
    test_c_1 = Custom(test_c_1_str)
    test_c_2_str = '012345'
    test_c_2 = Custom(test_c_2_str)
    test_c_3_str = 'foobar'
    test_c_3 = Custom(test_c_3_str)

    @dataclass_dict_convert(
        dict_letter_case=camelcase,
        custom_type_convertors=[SimpleTypeConvertor(
            type=Custom,
            to_dict=lambda c: c.c,
            from_dict=lambda c: Custom(c)
        )]
    )
    @dataclass(frozen=True)
    @dataclass_multiline_repr
    class Test:
        a_date: Custom
        an_opt: Optional[Custom]
        a_list: List[Custom]
        a_dict: Dict[str, Custom]

    the_instance = Test(test_c_1, test_c_2, [test_c_3], {'key': test_c_1})
    the_dict = {
        'aDate': test_c_1_str,
        'anOpt': test_c_2_str,
        'aList': [test_c_3_str],
        'aDict': {'key': test_c_1_str},
    }

    expected = the_dict
    actual = the_instance.to_dict()
    assert actual == expected

    expected = the_instance
    actual = Test.from_dict(the_dict)
    assert actual == expected


def test_dataclass_dict_Dict_convert_1():
    test_d_1 = {'foo': 'bar'}
    test_d_2 = {'foo2': 'bar2'}
    test_d_3 = {'foo3': 'bar3'}
    test_d_4 = {'foo4': 'bar4'}

    class TestBase(ABC):
        pass

    @dataclass_dict_convert(dict_letter_case=camelcase)
    @dataclass(frozen=True)
    class Test(TestBase):
        a_date: Dict
        an_opt: Optional[Dict] = None
        an_opt2: Optional[Dict] = None
        a_list: List[Dict] = dataclasses.field(default=list)
        a_dict: Dict[str, Dict] = dataclasses.field(default=dict)

    the_instance = Test(dict(test_d_1), dict(test_d_2), None, [dict(test_d_3)], {'key': dict(test_d_4)})
    the_dict = {
        'aDate': dict(test_d_1),
        'anOpt': dict(test_d_2),
        'anOpt2': None,
        'aList': [dict(test_d_3)],
        'aDict': {'key': dict(test_d_4)},
    }

    expected = the_dict
    actual = the_instance.to_dict()
    assert actual == expected

    expected = the_instance
    actual = Test.from_dict(the_dict)
    assert actual == expected


def test_dataclass_dict_convert_inheritance_1():
    @dataclass_dict_convert(dict_letter_case=camelcase)
    @dataclass(frozen=True)
    class CustomParent:
        a: str

    @dataclass_dict_convert(dict_letter_case=camelcase)
    @dataclass(frozen=True)
    class CustomChild(CustomParent):
        b: str

    the_instance = CustomChild('a1', 'b1')

    the_dict = {
        'a': 'a1',
        'b': 'b1',
    }

    expected = the_dict
    actual = the_instance.to_dict()
    assert actual == expected

    expected = the_instance
    actual = CustomChild.from_dict(the_dict)
    assert actual == expected


def test_dataclass_dict_convert_inheritance_2():
    @dataclass_dict_convert(dict_letter_case=camelcase)
    @dataclass(frozen=True)
    class CustomParent:
        a: str
        b: int = 1

    @dataclass_dict_convert(dict_letter_case=camelcase)
    @dataclass(frozen=True)
    class CustomChild(CustomParent):
        c: str = 'blah'
        d: int = 5

    the_instance = CustomChild(a='a1', b=2, c='c1', d=3)

    the_dict = {
        'a': 'a1',
        'b': 2,
        'c': 'c1',
        'd': 3,
    }

    expected = the_dict
    actual = the_instance.to_dict()
    assert actual == expected

    expected = the_instance
    actual = CustomChild.from_dict(the_dict)
    assert actual == expected


def test_dataclass_dict_convert_extra_defaults_1():
    @dataclass_dict_convert(
        dict_letter_case=camelcase,
        extra_field_defaults={}
    )
    @dataclass(frozen=True)
    class Test:
        an_int: int
        a_str: str
        a_float: float
        a_bool: bool

    the_instance = Test(1, 'foo', 0.1, True)
    the_dict = {
        'anInt': 1,
        'aStr': 'foo',
        #'aFloat': 0.1,
        #'aBool': True,
    }

    assert 'anInt' == camelcase('an_int')

    expected = the_instance
    with pytest.raises(TypeError):
        actual = Test.from_dict(the_dict)
    # assert actual == expected


def test_dataclass_dict_convert_extra_defaults_2():
    @dataclass_dict_convert(
        dict_letter_case=camelcase,
        extra_field_defaults={
            'a_float': 0.1,
            'a_bool': lambda: True,
        }
    )
    @dataclass(frozen=True)
    class Test:
        an_int: int
        a_str: str
        a_float: float
        a_bool: bool

    the_instance = Test(1, 'foo', 0.1, True)
    the_dict = {
        'anInt': 1,
        'aStr': 'foo',
        #'aFloat': 0.1,
        #'aBool': True,
    }

    assert 'anInt' == camelcase('an_int')

    expected = the_instance
    actual = Test.from_dict(the_dict)
    assert actual == expected


def test_dataclass_dict_convert_extra_defaults_3():
    @dataclass_dict_convert(
        dict_letter_case=camelcase,
        extra_field_defaults={
            'bad': 10.0,
        }
    )
    @dataclass(frozen=True)
    class Test:
        an_int: int
        a_str: str
        a_float: float
        a_bool: bool

    the_instance = Test(1, 'foo', 0.1, True)
    the_dict = {
        'anInt': 1,
        'aStr': 'foo',
        'aFloat': 0.1,
        'aBool': True,
    }

    assert 'anInt' == camelcase('an_int')

    expected = the_instance
    with pytest.raises(UnknownFieldError):
        actual = Test.from_dict(the_dict)


def test_dataclass_dict_convert_extra_defaults_inherit_1():
    @dataclass_dict_convert(
        dict_letter_case=camelcase,
        extra_field_defaults={}
    )
    @dataclass(frozen=True)
    class TestA:
        a_str: str
        a_str2: str

    @dataclass_dict_convert(
        dict_letter_case=camelcase,
    )
    @dataclass(frozen=True)
    class TestB(TestA):
        an_int: int

    the_instance = TestB('blah', 'b', 3)
    the_dict = {
        'anInt': 3,
        # 'aStr': 'blab',
        'aStr2': 'b',
    }

    expected = the_instance
    with pytest.raises(TypeError):
        actual = TestB.from_dict(the_dict)


def test_dataclass_dict_convert_extra_defaults_inherit_2():
    @dataclass_dict_convert(
        dict_letter_case=camelcase,
        extra_field_defaults={
            'a_str': 'blah'
        }
    )
    @dataclass(frozen=True)
    class TestA:
        a_str: str
        a_str2: str

    @dataclass_dict_convert(
        dict_letter_case=camelcase,
    )
    @dataclass(frozen=True)
    class TestB(TestA):
        an_int: int

    the_instance = TestB('blah', 'b', 3)
    the_dict = {
        'anInt': 3,
        # 'aStr': 'blab',
        'aStr2': 'b',
    }

    expected = the_instance
    actual = TestB.from_dict(the_dict)
    assert actual == expected


def test_dataclass_dict_convert_unknown_field_1():
    @dataclass_dict_convert(dict_letter_case=camelcase,)
    @dataclass(frozen=True)
    class Test:
        an_int: int

    the_instance = Test(1)
    the_dict = {
        'anInt': 1,
        'aStr': 'foo',
    }

    with pytest.raises(UnknownFieldError):
        actual = Test.from_dict(the_dict)


def test_dataclass_dict_convert_unknown_field_2():
    called_unknown = False

    def unknown_handler(fieldname: str):
        nonlocal called_unknown
        assert fieldname == 'aStr'
        called_unknown = True

    @dataclass_dict_convert(
        dict_letter_case=camelcase,
        on_unknown_field=unknown_handler
    )
    @dataclass(frozen=True)
    class Test:
        an_int: int

    the_instance = Test(1)
    the_dict = {
        'anInt': 1,
        'aStr': 'foo',
    }

    actual = Test.from_dict(the_dict)
    assert actual == the_instance

    assert called_unknown


def test_dataclass_dict_convert_nested_unknown_field_override_1a():
    called_unknown_1 = False
    called_unknown_2 = False

    def unknown_handler(fieldname: str):
        nonlocal called_unknown_1
        nonlocal called_unknown_2
        assert fieldname in ('aStr1', 'aStr2')
        if fieldname == 'aStr1':
            called_unknown_1 = True
        if fieldname == 'aStr2':
            called_unknown_2 = True

    @dataclass_dict_convert(
        dict_letter_case=camelcase,
    )
    @dataclass(frozen=True)
    class TestB:
        an_int2: int

    @dataclass_dict_convert(
        dict_letter_case=camelcase
    )
    @dataclass(frozen=True)
    class Test:
        an_int: int
        b: TestB

    the_instance = Test(1, TestB(2))
    the_dict = {
        'anInt': 1,
        'aStr1': 'foo',
        'b': {
            'anInt2': 2,
            'aStr2': 'bar',
        }
    }

    actual = Test.from_dict(the_dict, on_unknown_field_override=unknown_handler)
    assert actual == the_instance

    assert called_unknown_1
    assert called_unknown_2


def test_dataclass_dict_convert_nested_unknown_field_override_1b():
    @dataclass_dict_convert(
        dict_letter_case=camelcase,
    )
    @dataclass(frozen=True)
    class TestB:
        an_int2: int

    @dataclass_dict_convert(
        dict_letter_case=camelcase
    )
    @dataclass(frozen=True)
    class Test:
        an_int: int
        b: TestB

    the_instance = Test(1, TestB(2))
    the_dict = {
        'anInt': 1,
        'aStr1': 'foo',
        'b': {
            'anInt2': 2,
            'aStr2': 'bar',
        }
    }

    from dataclass_dict_convert.convert import ignore_unknown_fields
    actual = Test.from_dict(the_dict, on_unknown_field_override=ignore_unknown_fields)
    assert actual == the_instance


def test_dataclass_dict_convert_nested_unknown_field_override_1c():
    called_unknown_1 = False
    called_unknown_2 = False

    def unknown_handler(fieldname: str):
        nonlocal called_unknown_1
        nonlocal called_unknown_2
        assert fieldname in ('aStr1', 'aStr2')
        if fieldname == 'aStr1':
            called_unknown_1 = True
        if fieldname == 'aStr2':
            called_unknown_2 = True

    @dataclass_dict_convert(
        dict_letter_case=camelcase,
    )
    @dataclass(frozen=True)
    class TestB:
        an_int2: int

    @dataclass_dict_convert(
        dict_letter_case=camelcase
    )
    @dataclass(frozen=True)
    class Test:
        an_int: int
        b: TestB

    the_instance = Test(1, TestB(2))
    the_dict = {
        'anInt': 1,
        'aStr1': 'foo',
        'b': {
            'anInt2': 2,
            'aStr2': 'bar',
        }
    }

    actual = Test.from_json(json.dumps(the_dict), on_unknown_field_override=unknown_handler)
    assert actual == the_instance

    assert called_unknown_1
    assert called_unknown_2


def test_dataclass_dict_convert_nested_unknown_field_override_2a():
    called_unknown_1 = False
    called_unknown_2 = False

    def unknown_handler(fieldname: str):
        nonlocal called_unknown_1
        nonlocal called_unknown_2
        assert fieldname in ('aStr1', 'aStr2')
        if fieldname == 'aStr1':
            called_unknown_1 = True
        if fieldname == 'aStr2':
            called_unknown_2 = True

    @dataclass_dict_convert(
        dict_letter_case=camelcase,
    )
    @dataclass(frozen=True)
    class TestB:
        an_int2: int

    @dataclass_dict_convert(
        dict_letter_case=camelcase
    )
    @dataclass(frozen=True)
    class Test:
        an_int: int
        b: List[TestB]

    the_instance = Test(1, [TestB(2)])
    the_dict = {
        'anInt': 1,
        'aStr1': 'foo',
        'b': [{
            'anInt2': 2,
            'aStr2': 'bar',
        }]
    }

    actual = Test.from_dict(the_dict, on_unknown_field_override=unknown_handler)
    assert actual == the_instance

    assert called_unknown_1
    assert called_unknown_2


def test_dataclass_dict_convert_nested_unknown_field_override_2b():
    called_unknown_1 = 0
    called_unknown_2 = 0

    def unknown_handler(fieldname: str):
        nonlocal called_unknown_1
        nonlocal called_unknown_2
        assert fieldname in ('aStr1', 'aStr2')
        if fieldname == 'aStr1':
            called_unknown_1 += 1
        if fieldname == 'aStr2':
            called_unknown_2 += 1

    @dataclass_dict_convert(
        dict_letter_case=camelcase,
    )
    @dataclass(frozen=True)
    class TestB:
        an_int2: int

    @dataclass_dict_convert(
        dict_letter_case=camelcase
    )
    @dataclass(frozen=True)
    class Test:
        an_int: int
        b: List[TestB]

    the_instance = Test(1, [TestB(2), TestB(3)])
    the_dict = {
        'anInt': 1,
        'aStr1': 'foo',
        'b': [{
            'anInt2': 2,
            'aStr2': 'bar',
        }, {
            'anInt2': 3,
            'aStr2': 'bar',
        }]
    }

    actual = Test.from_dict(the_dict, on_unknown_field_override=unknown_handler)
    assert actual == the_instance

    assert called_unknown_1 == 1
    assert called_unknown_2 == 2


def test_dataclass_dict_convert_nested_unknown_field_override_3():
    called_unknown_1 = 0
    called_unknown_2 = 0

    def unknown_handler(fieldname: str):
        nonlocal called_unknown_1
        nonlocal called_unknown_2
        assert fieldname in ('aStr1', 'aStr2')
        if fieldname == 'aStr1':
            called_unknown_1 += 1
        if fieldname == 'aStr2':
            called_unknown_2 += 1

    @dataclass_dict_convert(
        dict_letter_case=camelcase,
    )
    @dataclass(frozen=True)
    class TestB:
        an_int2: int

    @dataclass_dict_convert(
        dict_letter_case=camelcase
    )
    @dataclass(frozen=True)
    class Test:
        an_int: int
        b: List[TestB]

    the_instance1 = Test(1, [TestB(2)])
    the_instance2 = Test(3, [TestB(4)])
    the_dict1 = {
        'anInt': 1,
        'aStr1': 'foo',
        'b': [{
            'anInt2': 2,
            'aStr2': 'bar',
        }]
    }
    the_dict2 = {
        'anInt': 3,
        'aStr1': 'foo2',
        'b': [{
            'anInt2': 4,
            'aStr2': 'bar2',
        }]
    }

    actual = Test.from_dict_list([the_dict1, the_dict2], on_unknown_field_override=unknown_handler)
    assert actual == [the_instance1, the_instance2]

    assert called_unknown_1 == 2
    assert called_unknown_2 == 2


def test_dataclass_dict_convert_preprocess_1():
    def pp(d: Dict) -> Dict:
        d = dict(d)
        keys = list(d.keys())
        for key in keys:
            if key.startswith('REMOVEME'):
                new_key = key[8:]
                d[new_key] = d[key]
                del d[key]
        return d

    @dataclass_dict_convert(
        dict_letter_case=camelcase,
        preprocess_from_dict=pp
    )
    @dataclass(frozen=True)
    class Test:
        an_int: int
        a_str: str
        a_float: float
        a_bool: bool

    the_instance = Test(1, 'foo', 0.1, True)
    the_dict = {
        'anInt': 1,
        'aStr': 'foo',
        'aFloat': 0.1,
        'aBool': True,
    }
    the_dict2 = {
        'REMOVEMEanInt': 1,
        'REMOVEMEaStr': 'foo',
        'REMOVEMEaFloat': 0.1,
        'REMOVEMEaBool': True,
    }

    assert 'anInt' == camelcase('an_int')

    expected = the_dict
    actual = the_instance.to_dict()
    assert actual == expected

    expected = the_instance
    actual = Test.from_dict(the_dict)
    assert actual == expected

    expected = the_instance
    actual = Test.from_dict(the_dict2)
    assert actual == expected


def test_dataclass_dict_convert_preprocess_2():
    def pp(d: Dict) -> Dict:
        keys = list(d.keys())
        for key in keys:
            if key.startswith('REMOVEME'):
                new_key = key[8:]
                d[new_key] = d[key]
                del d[key]
        return d

    @dataclass_dict_convert(
        dict_letter_case=camelcase,
        preprocess_from_dict=pp
    )
    @dataclass(frozen=True)
    class Test:
        an_int: int
        a_str: str
        a_float: float
        a_bool: bool

    the_instance = Test(1, 'foo', 0.1, True)
    the_dict = {
        'anInt': 1,
        'aStr': 'foo',
        'aFloat': 0.1,
        'aBool': True,
    }
    the_dict2 = {
        'REMOVEMEanInt': 1,
        'aStr': 'foo',
        'REMOVEMEaFloat': 0.1,
        'aBool': True,
    }

    assert 'anInt' == camelcase('an_int')

    expected = the_dict
    actual = the_instance.to_dict()
    assert actual == expected

    expected = the_instance
    actual = Test.from_dict(the_dict)
    assert actual == expected

    expected = the_instance
    actual = Test.from_dict(the_dict2)
    assert actual == expected


def test_dataclass_dict_convert_preprocess_3():
    def pp(d: Dict) -> Dict:
        keys = list(d.keys())
        for key in keys:
            if key.startswith('REMOVEME'):
                new_key = key[8:]
                d[new_key] = d[key]
                del d[key]
        return d

    @dataclass_dict_convert(
        dict_letter_case=camelcase,
        preprocess_from_dict=pp
    )
    @dataclass(frozen=True)
    class Test:
        an_int: int
        a_str: str
        a_float: float
        a_bool: bool

    the_instance = Test(1, 'foo', 0.1, True)
    the_dict = {
        'anInt': 1,
        'aStr': 'foo',
        'aFloat': 0.1,
        'aBool': True,
    }
    the_dict2 = {
        'REMOVEMEanInt': 1,
        'aStr': 'foo',
        'REMOVEMEaFloat': 0.1,
        'aBool': True,
    }

    assert 'anInt' == camelcase('an_int')

    expected = the_dict
    actual = the_instance.to_dict()
    assert actual == expected

    expected = the_instance
    actual = Test.from_json(json.dumps(the_dict))
    assert actual == expected

    expected = the_instance
    actual = Test.from_json(json.dumps(the_dict2))
    assert actual == expected


def test_dataclass_dict_convert_postprocess_1():
    def pp(d: Dict) -> Dict:
        d = dict(d)
        if 'anInt' in d:
            d['anInt'] = d['anInt'] + 1
        if 'aStr' in d:
            d['aStrPlus'] = d['aStr'] + '++'
            del d['aStr']
        d['postModified'] = True
        return d

    @dataclass_dict_convert(
        dict_letter_case=camelcase,
        postprocess_to_dict=pp
    )
    @dataclass(frozen=True)
    class Test:
        an_int: int
        a_str: str
        a_float: float
        a_bool: bool

    the_instance = Test(1, 'foo', 0.1, True)
    the_dict = {
        'anInt': 1,
        'aStr': 'foo',
        'aFloat': 0.1,
        'aBool': True,
    }
    the_dict2 = {
        'anInt': 2,
        'aStrPlus': 'foo++',
        'aFloat': 0.1,
        'aBool': True,
        'postModified': True,
    }

    expected = the_dict2
    actual = the_instance.to_dict()
    assert actual == expected

    expected = json.dumps(the_dict2)
    actual = the_instance.to_json()
    assert json.loads(actual) == json.loads(expected)

    expected = the_instance
    actual = Test.from_dict(the_dict)
    assert actual == expected


def test_dataclass_dict_convert_alt_letter_case_1():
    @dataclass_dict_convert(
        dict_letter_case=camelcase,
        alt_dict_letter_case=snakecase,
    )
    @dataclass(frozen=True)
    class Test:
        an_int: int
        a_str: str
        a_float: float
        a_bool: bool

    the_instance = Test(1, 'foo', 0.1, True)
    the_dict = {
        'anInt': 1,
        'aStr': 'foo',
        'aFloat': 0.1,
        'aBool': True,
    }
    the_dict_alt = {
        'an_int': 1,
        'a_str': 'foo',
        'a_float': 0.1,
        'a_bool': True,
    }

    assert 'anInt' == camelcase('an_int')
    assert 'an_int' == snakecase('an_int')

    # regular case test

    expected = the_dict
    actual = the_instance.to_dict()
    assert actual == expected

    expected = the_instance
    actual = Test.from_dict(the_dict)
    assert actual == expected

    # ALT case test

    expected = the_dict_alt
    actual = the_instance.to_dict(alt_case=True)
    assert actual == expected

    expected = the_instance
    actual = Test.from_dict(the_dict_alt)
    assert actual == expected


def test_dataclass_dict_convert_alt_letter_case_2_composition():
    @dataclass_dict_convert(
        dict_letter_case=camelcase,
        alt_dict_letter_case=snakecase,
    )
    @dataclass(frozen=True)
    class TestB:
        an_int: int
        a_str: str
        a_float: float
        a_bool: bool

    @dataclass_dict_convert(
        dict_letter_case=camelcase,
        alt_dict_letter_case=snakecase,
    )
    @dataclass(frozen=True)
    class Test:
        nestedClass: TestB
        nestedInOpt: Optional[TestB]
        nestedInList: List[TestB]

    the_instanceB1 = TestB(1, 'foo', 0.1, True)
    the_instanceB2 = TestB(2, 'bar', 0.2, False)
    the_instanceB3 = TestB(3, 'baz', 0.3, True)
    the_instanceB4 = TestB(4, 'huh', 0.4, False)
    the_instance = Test(the_instanceB1, the_instanceB2, [the_instanceB3, the_instanceB4])
    the_dict = {
        'nestedClass': {'anInt': 1, 'aStr': 'foo', 'aFloat': 0.1, 'aBool': True,},
        'nestedInOpt': {'anInt': 2, 'aStr': 'bar', 'aFloat': 0.2, 'aBool': False,},
        'nestedInList': [
            {'anInt': 3, 'aStr': 'baz', 'aFloat': 0.3, 'aBool': True, },
            {'anInt': 4, 'aStr': 'huh', 'aFloat': 0.4, 'aBool': False, },
        ],
    }
    the_dict_alt = {
        'nested_class': {'an_int': 1, 'a_str': 'foo', 'a_float': 0.1, 'a_bool': True,},
        'nested_in_opt': {'an_int': 2, 'a_str': 'bar', 'a_float': 0.2, 'a_bool': False,},
        'nested_in_list': [
            {'an_int': 3, 'a_str': 'baz', 'a_float': 0.3, 'a_bool': True, },
            {'an_int': 4, 'a_str': 'huh', 'a_float': 0.4, 'a_bool': False, },
        ],
    }

    # regular case test
    expected = the_dict
    actual = the_instance.to_dict()
    assert actual == expected

    expected = the_instance
    actual = Test.from_dict(the_dict)
    assert actual == expected

    # ALT case test

    expected = the_dict_alt
    actual = the_instance.to_dict(alt_case=True)
    assert actual == expected

    expected = the_instance
    actual = Test.from_dict(the_dict_alt)
    assert actual == expected


def test_dataclass_multiline_repr_1():
    @dataclass_dict_convert(
        dict_letter_case=camelcase
    )
    @dataclass(frozen=True)
    @dataclass_multiline_repr
    class Test:
        an_int: int
        a_str: str
        a_float: float
        a_bool: bool

    the_instance = Test(1, 'foo', 0.1, True)
    expected = 'test_dataclass_multiline_repr_1.<locals>.Test(\n' \
               '   an_int=1,\n' \
               '   a_str=\'foo\',\n' \
               '   a_float=0.1,\n' \
               '   a_bool=True)'

    actual = repr(the_instance)
    assert actual == expected

    actual = f'{the_instance!r}'
    assert actual == expected


def test_dataclass_multiline_str_1():
    @dataclass_dict_convert(
        dict_letter_case=camelcase
    )
    @dataclass(frozen=True)
    @dataclass_multiline_repr
    class Test:
        an_int: int
        a_str: str
        a_float: float
        a_bool: bool

        def __str__(self):
            return repr(self)

    the_instance = Test(1, 'foo', 0.1, True)
    expected = 'test_dataclass_multiline_str_1.<locals>.Test(\n' \
               '   an_int=1,\n' \
               '   a_str=\'foo\',\n' \
               '   a_float=0.1,\n' \
               '   a_bool=True)'

    actual = repr(the_instance)
    assert actual == expected

    actual = f'{the_instance!r}'
    assert actual == expected

    actual = str(the_instance)
    assert actual == expected

    actual = f'{the_instance}'
    assert actual == expected


def _test_to_from(obj, Cls):
    d = obj.to_dict()
    actual = Cls.from_dict(d)
    assert actual == obj

    d2 = actual.to_dict()
    actual2 = Cls.from_dict(d2)
    assert actual2 == obj


def test_any_simple_1():
    @dataclass_dict_convert(dict_letter_case=camelcase)
    @dataclass(frozen=True)
    class Foo:
        bar: Any

    _test_to_from(Foo({'bar': 'baz'}), Foo)
    _test_to_from(Foo({'bar': 1}), Foo)
    _test_to_from(Foo({'bar': 1.2}), Foo)
    _test_to_from(Foo({'bar': True}), Foo)


def test_any_complex_1():
    @dataclass_dict_convert(dict_letter_case=camelcase)
    @dataclass(frozen=True)
    class Foo:
        bar: Any

    _test_to_from(Foo({'bar': ['foo', 'bar']}), Foo)
    _test_to_from(Foo({'bar': [1, 2, 3]}), Foo)
    _test_to_from(Foo({'bar': [1.2, 2.3, 3.4]}), Foo)
    _test_to_from(Foo({'bar': {'a': 1, 'b': 2, 'c': 3}}), Foo)
    _test_to_from(Foo({'bar': {'a': 'x', 'b': 'y', 'c': 'z'}}), Foo)
    _test_to_from(Foo({'bar': [{'a': 1}, {'b': 2}, {'c': 3}]}), Foo)


def test_any_complex_mix_1():
    @dataclass_dict_convert(dict_letter_case=camelcase)
    @dataclass(frozen=True)
    class Foo:
        bar: Any

    _test_to_from(Foo({'bar': [1.2, 3, 'baz', False]}), Foo)
    _test_to_from(Foo({'bar': {'a': 1, 'b': 'c', 'c': 1.2, 'd': True}}), Foo)
    _test_to_from(Foo({'bar': [{'a': 1, 'b': 'c', 'c': 1.2}, 2, False]}), Foo)

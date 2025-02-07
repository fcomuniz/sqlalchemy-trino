import pytest
from assertpy import assert_that
from sqlalchemy.sql.sqltypes import *
from sqlalchemy.sql.type_api import TypeEngine

from sqlalchemy_trino import datatype
from sqlalchemy_trino.datatype import MAP, ROW


@pytest.mark.parametrize(
    'type_str, sql_type',
    datatype._type_map.items(),
    ids=datatype._type_map.keys()
)
def test_parse_simple_type(type_str: str, sql_type: TypeEngine):
    actual_type = datatype.parse_sqltype(type_str)
    if not isinstance(actual_type, type):
        actual_type = type(actual_type)
    assert_that(actual_type).is_equal_to(sql_type)


parse_type_options_testcases = {
    'VARCHAR(10)': VARCHAR(10),
    'DECIMAL(20)': DECIMAL(20),
    'DECIMAL(20, 3)': DECIMAL(20, 3),
}


@pytest.mark.parametrize(
    'type_str, sql_type',
    parse_type_options_testcases.items(),
    ids=parse_type_options_testcases.keys()
)
def test_parse_type_options(type_str: str, sql_type: TypeEngine):
    actual_type = datatype.parse_sqltype(type_str)
    assert_that(actual_type).is_sqltype(sql_type)


parse_array_testcases = {
    'array(integer)': ARRAY(INTEGER()),
    'array(varchar(10))': ARRAY(VARCHAR(10)),
    'array(decimal(20,3))': ARRAY(DECIMAL(20, 3)),
    'array(array(varchar(10)))': ARRAY(VARCHAR(10), dimensions=2),
}


@pytest.mark.parametrize(
    'type_str, sql_type',
    parse_array_testcases.items(),
    ids=parse_array_testcases.keys()
)
def test_parse_array(type_str: str, sql_type: ARRAY):
    actual_type = datatype.parse_sqltype(type_str)
    assert_that(actual_type).is_sqltype(sql_type)


parse_map_testcases = {
    'map(char, integer)': MAP(CHAR(), INTEGER()),
    'map(varchar(10), varchar(10))': MAP(VARCHAR(10), VARCHAR(10)),
    'map(varchar(10), decimal(20,3))': MAP(VARCHAR(10), DECIMAL(20, 3)),
    'map(char, array(varchar(10)))': MAP(CHAR(), ARRAY(VARCHAR(10))),
    'map(varchar(10), array(varchar(10)))': MAP(VARCHAR(10), ARRAY(VARCHAR(10))),
    'map(varchar(10), array(array(varchar(10))))': MAP(VARCHAR(10), ARRAY(VARCHAR(10), dimensions=2)),
}


@pytest.mark.parametrize(
    'type_str, sql_type',
    parse_map_testcases.items(),
    ids=parse_map_testcases.keys()
)
def test_parse_map(type_str: str, sql_type: ARRAY):
    actual_type = datatype.parse_sqltype(type_str)
    assert_that(actual_type).is_sqltype(sql_type)


parse_row_testcases = {
    'row(a integer, b varchar)': ROW(dict(a=INTEGER(), b=VARCHAR())),
    'row(a varchar(20), b decimal(20,3))': ROW(dict(a=VARCHAR(20), b=DECIMAL(20, 3))),
    'row(x array(varchar(10)), y array(array(varchar(10))), z decimal(20,3))':
        ROW(dict(x=ARRAY(VARCHAR(10)), y=ARRAY(VARCHAR(10), dimensions=2), z=DECIMAL(20, 3))),
    'row(min timestamp(6) with time zone, max timestamp(6) with time zone, null_count bigint)':
        ROW(dict(min=TIMESTAMP(), max=TIMESTAMP(), null_count=BIGINT())),
}


@pytest.mark.parametrize(
    'type_str, sql_type',
    parse_row_testcases.items(),
    ids=parse_row_testcases.keys()
)
def test_parse_row(type_str: str, sql_type: ARRAY):
    actual_type = datatype.parse_sqltype(type_str)
    assert_that(actual_type).is_sqltype(sql_type)


parse_datetime_testcases = {
    'date': DATE(),
    'time': TIME(),
    'time with time zone': TIME(timezone=True),
    'timestamp': TIMESTAMP(),
    'timestamp with time zone': TIMESTAMP(timezone=True),
}


@pytest.mark.parametrize(
    'type_str, sql_type',
    parse_datetime_testcases.items(),
    ids=parse_datetime_testcases.keys()
)
def test_parse_datetime(type_str: str, sql_type: ARRAY):
    actual_type = datatype.parse_sqltype(type_str)
    assert_that(actual_type).is_sqltype(sql_type)

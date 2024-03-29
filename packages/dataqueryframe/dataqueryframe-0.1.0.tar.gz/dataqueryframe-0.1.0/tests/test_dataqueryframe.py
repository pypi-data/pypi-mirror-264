# tests/test_dataqueryframe.py
import pandas as pd
import pytest
from dataqueryframe.dataqueryframe import DataQueryFrame

def test_print_code_empty():
    with pytest.raises(ValueError) as e:
        DataQueryFrame.print_code("")
    assert "No code string provided to print_code." in str(e.value)

def test_print_code_long():
    long_code = "a" * 1500
    DataQueryFrame.print_code(long_code)
    # No assertion needed, just checking if it runs without errors

def test_select_columns():
    data = {'col1': [1, 2], 'col2': [3, 4]}
    df = DataQueryFrame(data)
    result = df.select_columns(['col1'])
    expected = DataQueryFrame({'col1': [1, 2]})
    pd.testing.assert_frame_equal(result, expected)

def test_select_columns_missing():
    data = {'col1': [1, 2], 'col2': ['a', 'b']}
    df = DataQueryFrame(data)
    with pytest.raises(ValueError) as e:
        df.select_columns(['col3'])
    assert "Columns not found in DataFrame: ['col3']" in str(e.value)

def test_select_columns_single_string():
    data = {'col1': [1, 2], 'col2': [3, 4]}
    df = DataQueryFrame(data)
    result = df.select_columns('col1')
    expected = DataQueryFrame({'col1': [1, 2]})
    pd.testing.assert_frame_equal(result, expected)

def test_select_distinct_single_string():
    data = {'col1': [1, 1, 2], 'col2': [3, 3, 4]}
    df = DataQueryFrame(data)
    result = df.select_distinct('col1')
    expected = DataQueryFrame({'col1': [1, 2], 'col2': [3, 4]})
    pd.testing.assert_frame_equal(result.reset_index(drop=True), expected)

def test_select_count_distinct_single_string():
    data = {'col1': [1, 1, 2], 'col2': ['a', 'a', 'b']}
    df = DataQueryFrame(data)
    result = df.select_count(distinct=True, distinct_columns='col2')
    expected = DataQueryFrame({'count': [2]})
    pd.testing.assert_frame_equal(result, expected)

def test_select_count():
    data = {'col1': [1, 1, 2], 'col2': ['a', 'a', 'b']}
    df = DataQueryFrame(data)
    result = df.select_count(group_by='col1')
    expected = DataQueryFrame({'col1': [1, 2], 'count': [2, 1]})
    pd.testing.assert_frame_equal(result, expected)

def test_select_count_no_groupby():
    data = {'col1': [1, 2, 3], 'col2': ['a', 'b', 'c']}
    df = DataQueryFrame(data)
    result = df.select_count()
    expected = DataQueryFrame({'count': [3]})
    pd.testing.assert_frame_equal(result, expected)

def test_select_count_distinct():
    data = {'col1': [1, 1, 2], 'col2': ['a', 'a', 'b']}
    df = DataQueryFrame(data)
    result = df.select_count(distinct=True, distinct_columns=['col2'])
    expected = DataQueryFrame({'count': [2]})
    pd.testing.assert_frame_equal(result, expected)

def test_select_count_distinct_error():
    data = {'col1': [1, 1, 2], 'col2': ['a', 'a', 'b']}
    df = DataQueryFrame(data)
    with pytest.raises(ValueError) as e:
        df.select_count(distinct=True)
    assert "When 'distinct' is True, 'distinct_columns' cannot be None." in str(e.value)

def test_select_count_distinct_columns_error():
    data = {'col1': [1, 1, 2], 'col2': ['a', 'a', 'b']}
    df = DataQueryFrame(data)
    with pytest.raises(ValueError) as e:
        df.select_count(distinct_columns=['col2'])
    assert "'distinct_columns' should only be set when 'distinct' is True." in str(e.value)

def test_select_distinct():
    data = {'col1': [1, 1, 2], 'col2': [3, 3, 4]}
    df = DataQueryFrame(data)
    result = df.select_distinct(['col1'])
    expected = DataQueryFrame({'col1': [1, 2], 'col2': [3, 4]})
    pd.testing.assert_frame_equal(result.reset_index(drop=True), expected)

def test_where_like():
    data = {'col1': ['apple', 'banana', 'cherry']}
    df = DataQueryFrame(data)
    result = df.where('col1', 'LIKE', 'a%')
    expected = DataQueryFrame({'col1': ['apple', 'banana']}, index=[0, 1])
    pd.testing.assert_frame_equal(result, expected)

def test_where_equals():
    data = {'col1': [1, 2, 3], 'col2': ['a', 'b', 'c']}
    df = DataQueryFrame(data)
    result = df.where('col1', '=', 2)
    expected = DataQueryFrame({'col1': [2], 'col2': ['b']}, index=[1])
    pd.testing.assert_frame_equal(result, expected)

def test_where_not_equals():
    data = {'col1': [1, 2, 3], 'col2': ['a', 'b', 'c']}
    df = DataQueryFrame(data)
    result = df.where('col1', '!=', 2)
    expected = DataQueryFrame({'col1': [1, 3], 'col2': ['a', 'c']}, index=[0, 2])
    pd.testing.assert_frame_equal(result, expected)

def test_where_invalid_operator():
    data = {'col1': [1, 2, 3], 'col2': ['a', 'b', 'c']}
    df = DataQueryFrame(data)
    with pytest.raises(ValueError) as e:
        df.where('col1', '?', 2)
    assert "Unsupported operator '?'" in str(e.value)

def test_where_non_existent_column():
    data = {'col1': [1, 2, 3], 'col2': ['a', 'b', 'c']}
    df = DataQueryFrame(data)
    with pytest.raises(ValueError) as e:
        df.where('col3', '=', 2)
    assert "Column 'col3' does not exist in the DataFrame." in str(e.value)

def test_order_by():
    data = {'col1': [2, 3, 1], 'col2': ['b', 'c', 'a']}
    df = DataQueryFrame(data)
    result = df.order_by('col1')
    expected = DataQueryFrame({'col1': [1, 2, 3], 'col2': ['a', 'b', 'c']}, index=[2, 0, 1])
    pd.testing.assert_frame_equal(result, expected)

def test_order_by_descending():
    data = {'col1': [2, 3, 1], 'col2': ['b', 'c', 'a']}
    df = DataQueryFrame(data)
    result = df.order_by('col1', ascending=False)
    expected = DataQueryFrame({'col1': [3, 2, 1], 'col2': ['c', 'b', 'a']}, index=[1, 0, 2])
    pd.testing.assert_frame_equal(result, expected)

def test_union():
    data_a = {'col1': [1, 2], 'col2': ['a', 'b']}
    data_b = {'col1': [2, 3], 'col2': ['b', 'c']}
    df_a = DataQueryFrame(data_a)
    df_b = DataQueryFrame(data_b)
    result = df_a.union(df_b)
    expected_data = {'col1': [1, 2, 3], 'col2': ['a', 'b', 'c']}
    expected = DataQueryFrame(expected_data).reset_index(drop=True)
    pd.testing.assert_frame_equal(result.reset_index(drop=True), expected)

def test_union_non_dataframe():
    data = {'col1': [1, 2], 'col2': ['a', 'b']}
    df = DataQueryFrame(data)
    with pytest.raises(ValueError) as e:
        df.union([1, 2, 3])
    assert "The 'other' parameter must be a pandas DataFrame or an instance of DataQueryFrame." in str(e.value)

def test_union_non_matching_columns():
    data_a = {'col1': [1, 2], 'col2': ['a', 'b']}
    data_b = {'col1': [3, 4], 'col3': ['c', 'd']}
    df_a = DataQueryFrame(data_a)
    df_b = DataQueryFrame(data_b)
    with pytest.raises(ValueError) as e:
        df_a.union(df_b)
    assert "DataFrames must have the same columns for a union operation." in str(e.value)

def test_union_different_column_order():
    data_a = {'col1': [1, 2], 'col2': ['a', 'b']}
    data_b = {'col2': ['c', 'd'], 'col1': [3, 4]}
    df_a = DataQueryFrame(data_a)
    df_b = DataQueryFrame(data_b)
    with pytest.raises(ValueError) as e:
        df_a.union(df_b)
    assert "DataFrames must have exactly matching columns in the same order for a union operation." in str(e.value)
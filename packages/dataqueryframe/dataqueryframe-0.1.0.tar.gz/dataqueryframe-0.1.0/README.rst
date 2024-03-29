DataQueryFrame
===============

.. image:: https://img.shields.io/pypi/v/dataqueryframe.svg
    :target: https://pypi.python.org/pypi/dataqueryframe

.. image:: https://readthedocs.org/projects/dataqueryframe/badge/?version=latest
    :target: https://dataqueryframe.readthedocs.io/en/latest/?version=latest

.. image:: https://pyup.io/repos/github/jmccoll7/dataqueryframe/shield.svg
    :target: https://pyup.io/repos/github/jmccoll7/dataqueryframe/

DataQueryFrame is an enhanced DataFrame library that provides SQL-like capabilities for data manipulation and analysis. It extends the functionality of the popular pandas DataFrame, allowing you to perform common database operations directly on your data.

Features
--------

- SQL-like query operations: SELECT, WHERE, GROUP BY, ORDER BY, UNION, etc.
- Seamless integration with pandas DataFrame
- Easy-to-use API for data filtering, aggregation, and transformation
- Support for various data sources (CSV, Excel, SQL databases, etc.)
- Efficient and optimized for large datasets

Installation
------------

You can install DataQueryFrame using pip:

::

    pip install dataqueryframe

Usage
-----

Here's a quick example of how to use DataQueryFrame:

.. code-block:: python

    import pandas as pd
    from dataqueryframe.dataqueryframe import DataQueryFrame as dqf

    # Create a DataQueryFrame from a parquet file
    # df = dqf(pd.read_parquet('data.parquet'))

    # Create a DataQueryFrame from a dictionary
    df = dqf({'A': [1,2,3,4,5], 'B': ['good', 'bad', 'ugly', 'good', 'bad']})

    # Perform SQL-like operations
    result = df.select(['column1', 'column2']) \
               .where('column1', '<', 3) \
               .order_by('column1', ascending=False) \
               .limit(10)
    print(result)

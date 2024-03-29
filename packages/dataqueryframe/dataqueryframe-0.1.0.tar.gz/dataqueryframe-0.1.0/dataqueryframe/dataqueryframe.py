import pandas as pd
import re  # For sanitizing inputs for LIKE functionality
from typing import Union, List, Optional, Any


class DataQueryFrame(pd.DataFrame):
    @property
    def _constructor(self):
        return DataQueryFrame

    @staticmethod
    def print_code(code: str) -> None:
        """Prints the equivalent Python/pandas code for the executed SQL-like operation."""
        if not code:
            raise ValueError("No code string provided to print_code.")

        max_length = 1337
        if len(code) > max_length:
            truncated_code = code[:max_length] + "..."
            print(
                "The code is too long to display effectively. Showing the first part only:"
            )
            print(f"Python/pandas code: {truncated_code}\n")
        else:
            print(f"Python/pandas code: {code}\n")

    def _ensure_columns_exist(self, columns: List[str]) -> None:
        """
        Ensures that specified columns exist in the DataFrame.

        :param columns: A list of column names to check.
        :raises ValueError: If any specified column does not exist in the DataFrame.
        """
        missing_columns = [col for col in columns if col not in self.columns]
        if missing_columns:
            raise ValueError(f"Columns not found in DataFrame: {missing_columns}")

    def select(self, columns: Optional[Union[str, List[str]]] = None) -> "DataQueryFrame":
        """
        Selects specified columns, similar to SQL SELECT statement.

        :param columns: A string or list of strings representing column names to select.
        :return: A DataQueryFrame with only the specified columns.
        """
        if columns == "*":
            columns = None
        if columns:
            if isinstance(columns, str):
                columns = [columns]
            self._ensure_columns_exist(columns)
            code = f"df[{columns}])"
        else:
            code = "df"
        self.print_code(code)
        return (self[columns] if columns else self).pipe(DataQueryFrame)

    def select_distinct(self, columns: Optional[Union[str, List[str]]] = None) -> "DataQueryFrame":
        """
        Selects distinct rows based on specified columns, similar to SQL SELECT DISTINCT.

        :param columns: A string or list of strings representing column names for distinct selection.
        :return: A DataQueryFrame with distinct rows based on specified columns.
        """
        if columns == "*":
            columns = None
        if columns:
            if isinstance(columns, str):
                columns = [columns]
            self._ensure_columns_exist(columns)
            code = f"df.drop_duplicates(subset={columns})"
        else:
            code = "df.drop_duplicates()"
        self.print_code(code)
        return self.drop_duplicates(subset=columns).pipe(DataQueryFrame)
    
    def select_count(
        self,
        group_by: Optional[Union[str, List[str]]] = None,
        distinct: bool = False,
        distinct_columns: Optional[Union[str, List[str]]] = None,
    ) -> "DataQueryFrame":
        """
        Counts rows with an option for grouping and distinct count, similar to SQL COUNT function.

        :param group_by: Optional; a string or list of strings representing column names to group by.
        :param distinct: Optional; a boolean indicating whether to count distinct rows.
        :param distinct_columns: Optional; applicable if distinct is True, specifies columns for distinct count.
        :return: A DataQueryFrame with count results.
        """
        if distinct and distinct_columns is None:
            raise ValueError(
                "When 'distinct' is True, 'distinct_columns' cannot be None."
            )
        if not distinct and distinct_columns is not None:
            raise ValueError(
                "'distinct_columns' should only be set when 'distinct' is True."
            )

        if distinct:
            if isinstance(distinct_columns, str):
                distinct_columns = [distinct_columns]
            distinct_count = len(self.select_distinct(distinct_columns))
            result = pd.DataFrame({"count": [distinct_count]})
            code = f"len(df.select_distinct({distinct_columns}))"
        elif group_by is not None:
            if isinstance(group_by, str):
                group_by = [group_by]
            self._ensure_columns_exist(group_by)
            result = self.groupby(group_by).size().reset_index(name="count")
            code = f"df.groupby({group_by}).size().reset_index(name='count')"
        else:
            count_all = len(self)
            result = pd.DataFrame({"count": [count_all]})
            code = "len(df)  # Count all rows"

        self.print_code(code)
        return result.pipe(DataQueryFrame)

    def where(self, column: str, operator: str, value: Any) -> "DataQueryFrame":
        """
        Applies a conditional filter to the DataFrame, similar to SQL WHERE clause.

        :param column: The column name to apply the condition on.
        :param operator: The operator for the condition (e.g., '=', '!=', '<', '>', '<=', '>=', 'LIKE').
        :param value: The value to compare the column against.
        :return: A DataQueryFrame filtered based on the condition.
        """
        valid_operators = ["=", "!=", "<", ">", "<=", ">=", "LIKE"]
        if operator not in valid_operators:
            raise ValueError(
                f"Invalid operator '{operator}'. Valid operators are: {valid_operators}"
            )

        if column not in self.columns:
            raise ValueError(f"Column '{column}' does not exist in the DataFrame.")

        if operator.lower() == "like":
            # Sanitize input to avoid regex errors
            value = re.escape(value)
            # Replace '%' with '.*' for wildcard matching
            value = value.replace("%", ".*")
            condition = self[column].str.contains(value, case=False, na=False, regex=True)
            code = f"df[df['{column}'].str.contains('{value}', case=False, na=False, regex=True)]"
        elif operator == "=":
            condition = self[column] == value
            code = f"df[df['{column}'] == {value}]"
        else:
            condition = eval(f"self['{column}'] {operator} value")
            code = f"df[df['{column}'] {operator} {value}]"

        self.print_code(code)
        return self.loc[condition].pipe(DataQueryFrame)

    def order_by(
        self, columns: Union[str, List[str]], ascending: bool = True
    ) -> "DataQueryFrame":
        """
        Sorts the DataFrame based on specified column(s), similar to SQL ORDER BY clause.

        :param columns: A string or list of strings representing column names to sort by.
        :param ascending: Optional; a boolean indicating the sort direction (True for ascending, False for descending).
        :return: A DataQueryFrame sorted based on specified criteria.
        """
        if isinstance(columns, str):
            columns = [columns]
        self._ensure_columns_exist(columns)
        sorted_df = self.sort_values(by=columns, ascending=ascending)
        code = f"df.sort_values(by={columns}, ascending={ascending})"
        self.print_code(code)
        return sorted_df.pipe(DataQueryFrame)

    def union(self, other: pd.DataFrame) -> "DataQueryFrame":
        """
        Combines the result sets of this DataQueryFrame with another, including only distinct values,
        similar to SQL UNION operation.

        :param other: Another DataQueryFrame or pandas DataFrame to combine with.
        :return: A DataQueryFrame containing the union of the two DataFrames.
        """
        if not isinstance(other, pd.DataFrame):
            raise ValueError(
                "The 'other' parameter must be a pandas DataFrame or an instance of DataQueryFrame."
            )

        if set(self.columns) != set(other.columns):
            raise ValueError(
                "DataFrames must have the same columns for a union operation."
            )

        if list(self.columns) != list(other.columns):
            raise ValueError(
                "DataFrames must have exactly matching columns in the same order for a union operation."
            )

        result = (
            pd.concat([self, other], ignore_index=True)
            .drop_duplicates()
            .reset_index(drop=True)
        )

        code = "pd.concat([df, other], ignore_index=True).drop_duplicates().reset_index(drop=True)"
        self.print_code(code)

        return result.pipe(DataQueryFrame)

    def limit(self, n: int) -> "DataQueryFrame":
        """
        Limits the number of rows returned, similar to SQL LIMIT clause.

        :param n: An integer representing the maximum number of rows to return.
        :return: A DataQueryFrame limited to the specified number of rows.
        """
        limited_df = self.head(n)
        code = f"df.head({n})"
        self.print_code(code)
        return limited_df.pipe(DataQueryFrame)

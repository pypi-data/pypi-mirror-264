#
# Copyright 2024 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.

from typing import Any

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer


class SelectSingleColumnByHexName(ColumnTransformer):  # type: ignore[misc]
    """
    Select a single column from a data frame, based on a hex encoded column name.

    Parameters
    ----------
    hex_column_name : str
        Hex-encoded string representing the name of the column to select.

    impute_value : any, default ""
        Value to replace missing values with.

    Attributes
    ----------
    hex_column_name : str
        Stores the provided hex-encoded column name.

    hex_column_name : str
        Stores the column name, decoded from hex.

    impute_value : any
        Value to replace missing values with.

    Examples
    --------
    >>> import pandas as pd
    >>> from datarobotx.openblueprints.single_column_selector import SelectSingleColumnByHexName
    >>> df = pd.DataFrame({'diag_1': [1, 2, 3], 'other_column': [4, 5, 6]})
    >>> selector = SelectSingleColumnByHexName(hex_column_name='646961675f31')
    >>> print(selector.transform(df))
    """

    def __init__(
        self,
        hex_column_name: str,
        impute_value: Any = "",
    ) -> None:
        self.hex_column_name: str = hex_column_name
        self.column_name: str = bytes.fromhex(self.hex_column_name).decode("utf-8")
        self.impute_value: Any = impute_value
        super().__init__(
            [
                (
                    "select_column",
                    SimpleImputer(strategy="constant", fill_value=self.impute_value),
                    [self.column_name],
                )
            ]
        )

    def fit(self, X: pd.DataFrame, y: Any = None) -> "SelectSingleColumnByHexName":
        if self.column_name not in X.columns:
            raise ValueError(f"Error: Column '{self.column_name}' not found in X DataFrame.")
        super().fit(X, y)
        return self

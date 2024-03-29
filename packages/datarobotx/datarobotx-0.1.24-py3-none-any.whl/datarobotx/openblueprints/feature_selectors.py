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

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.feature_selection import SelectFromModel
from sklearn.linear_model import Lasso


def fill_na(X: Any) -> Any:
    if isinstance(X, pd.DataFrame):
        X_filled = X.fillna(0)
    else:
        X_filled = np.nan_to_num(X, nan=0)
    return X_filled


# mypy doesn't know how to type sklearn classes yet
class CustomSelectFromModel(SelectFromModel):  # type: ignore[misc]
    """
    A custom feature selection class that extends SelectFromModel, allowing the
    selection of different underlying estimators for feature selection.

    Parameters
    ----------
    model_type : str, optional (default='rf_regressor')
        Determines the type of model to use for feature selection.
        Options are:
        - 'rf_classifier' : RandomForestClassifier
        - 'rf_regressor' : RandomForestRegressor
        - 'lasso' : Lasso Regressor

    **kwargs :
        Additional keyword arguments to be passed to SelectFromModel.

    Attributes
    ----------
    model_type : str
        The type of model used for feature selection.

    estimator_ : BaseEstimator
        The fitted underlying estimator used for feature selection.

    Notes
    -----
    This class is a wrapper around SelectFromModel that simplifies switching between
    different underlying estimators.

    Examples
    --------
    >>> from sklearn.datasets import load_iris
    >>> X, y = load_iris(return_X_y=True)
    >>> selector = CustomSelectFromModel(model_type='rf_classifier')
    >>> selector.fit(X, y)
    >>> X_transformed = selector.transform(X)
    """

    def __init__(self, model_type: str = "rf_regressor", **kwargs: Any) -> None:
        self.model_type: str = model_type
        estimator: BaseEstimator = self._get_estimator()
        super().__init__(estimator=estimator, **kwargs)

    def _get_estimator(self) -> BaseEstimator:
        if self.model_type == "rf_regressor":
            return RandomForestRegressor()
        elif self.model_type == "rf_classifier":
            return RandomForestClassifier()
        elif self.model_type == "lasso":
            return Lasso()
        else:
            raise ValueError(
                "Invalid model type. Choose 'rf_classifier', 'rf_regressor', or 'lasso'."
            )

    def fit(self, X: Any, y: Any = None, **kwargs: Any) -> "CustomSelectFromModel":
        X_filled = fill_na(X)
        super().fit(X_filled, y, **kwargs)
        return self

    def transform(self, X: Any) -> Any:
        X_filled = fill_na(X)
        return super().transform(X_filled)

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

from typing import Any, Optional, Union

from sklearn.base import TransformerMixin
from sklearn.linear_model import ElasticNetCV, LogisticRegressionCV


class ElasticNetTransformerClassifer(LogisticRegressionCV, TransformerMixin):  # type: ignore[misc]
    """
    A custom transformer that extends LogisticRegressionCV to use its predictions
    as features for further modeling. This class allows the use of LogisticRegressionCV
    predictions within a scikit-learn pipeline.  Note that this can lead to overfitting.
    """

    def __init__(
        self,
        *,
        Cs: Any = 10,
        fit_intercept: bool = True,
        cv: Union[int, None] = None,
        dual: bool = False,
        penalty: str = "elasticnet",
        scoring: Union[str, None] = None,
        solver: str = "saga",
        tol: float = 1e-4,
        max_iter: int = 100,
        class_weight: Any = None,
        n_jobs: Union[int, None] = None,
        verbose: int = 0,
        refit: Union[bool, str] = True,
        intercept_scaling: float = 1.0,
        multi_class: str = "auto",
        random_state: Union[int, None] = None,
        l1_ratios: Any = None,
    ) -> None:
        if l1_ratios is None:
            l1_ratios = [0.5]
        LogisticRegressionCV.__init__(
            self,
            Cs=Cs,
            fit_intercept=fit_intercept,
            cv=cv,
            dual=dual,
            penalty=penalty,
            scoring=scoring,
            tol=tol,
            max_iter=max_iter,
            class_weight=class_weight,
            n_jobs=n_jobs,
            verbose=verbose,
            solver=solver,
            refit=refit,
            intercept_scaling=intercept_scaling,
            multi_class=multi_class,
            random_state=random_state,
            l1_ratios=l1_ratios,
        )

    def transform(self, X: Any) -> Any:
        """
        Applies the predict method of LogisticRegressionCV to the input features
        and reshapes the output for compatibility with scikit-learn transformers.

        Parameters
        ----------
        X : Union[np.ndarray, pd.DataFrame]
            The input features to transform.

        Returns
        -------
        np.ndarray
            The predictions from LogisticRegressionCV
        """
        return self.predict_proba(X)


class ElasticNetTransformerRegressor(ElasticNetCV, TransformerMixin):  # type: ignore[misc]
    """
    A custom transformer that extends LogisticRegressionCV to use its predictions
    as features for further modeling. This class allows the use of LogisticRegressionCV
    predictions within a scikit-learn pipeline.  Note that this can lead to overfitting.
    """

    def __init__(
        self,
        *,
        l1_ratio: Any = 0.5,
        eps: float = 1e-3,
        n_alphas: int = 100,
        alphas: Any = None,
        fit_intercept: bool = True,
        precompute: Any = "auto",
        max_iter: int = 1000,
        tol: float = 1e-4,
        cv: Optional[int] = None,
        copy_X: bool = True,
        verbose: int = 0,
        n_jobs: Optional[int] = None,
        positive: bool = False,
        random_state: Optional[int] = None,
        selection: str = "cyclic",
    ) -> None:
        ElasticNetCV.__init__(
            self,
            l1_ratio=l1_ratio,
            eps=eps,
            n_alphas=n_alphas,
            alphas=alphas,
            fit_intercept=fit_intercept,
            precompute=precompute,
            max_iter=max_iter,
            tol=tol,
            cv=cv,
            copy_X=copy_X,
            verbose=verbose,
            n_jobs=n_jobs,
            positive=positive,
            random_state=random_state,
            selection=selection,
        )

    def transform(self, X: Any) -> Any:
        """
        Applies the predict method of LogisticRegressionCV to the input features
        and reshapes the output for compatibility with scikit-learn transformers.

        Parameters
        ----------
        X : Union[np.ndarray, pd.DataFrame]
            The input features to transform.

        Returns
        -------
        np.ndarray
            The predictions from LogisticRegressionCV
        """
        return self.predict(X).reshape(-1, 1)

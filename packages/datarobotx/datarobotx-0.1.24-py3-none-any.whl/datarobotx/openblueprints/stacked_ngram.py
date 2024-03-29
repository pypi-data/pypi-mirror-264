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

from typing import Any, Callable, Union

from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import ElasticNet, LogisticRegression
from sklearn.pipeline import Pipeline
from vecstack import StackingTransformer


class StackedNgramClassifier(Pipeline):  # type: ignore[misc]
    """
    A simple and compact vext vectorizer. Selects a single text column (defined as a base64 encoded
    string) and tf-idf encodes it.

    Then fit a stacked logistic regression on top of it.

    Useful with tree based models like Xgboost.

    Parameters
    ----------
    lowercase : bool, default=True
        Convert all characters to lowercase before tokenizing.
    analyzer : {'word', 'char', 'char_wb'} or callable, default='word'
        Whether the feature should be made of word or character n-grams. Option ‘char_wb’ creates
        character n-grams only from text inside word boundaries; n-grams at the edges of words are
        padded with space. If a callable is passed it is used to extract the sequence of features
        out of the raw, unprocessed input.
    max_ngram : int, default=2
        The upper boundary of the range of n-values for different n-grams to be extracted. Only
        applies if analyzer is not callable.
    min_ngram : int, default=1
        The lower boundary of the range of n-values for different n-grams to be extracted. Only
        applies if analyzer is not callable.
    max_df : float or int, default=0.8
        When building the vocabulary ignore terms that have a document frequency strictly higher
        than the given threshold (corpus-specific stop words). If float in range [0.0, 1.0], the
        parameter represents a proportion of documents, integer absolute counts.
    min_df : float or int, default=2
        When building the vocabulary ignore terms that have a document frequency strictly lower than
        the given threshold. This value is also called cut-off in the literature. If float in range
        of [0.0, 1.0], the parameter represents a proportion of documents, integer absolute counts.
    max_features : int, default=20000
        If not None, build a vocabulary that only consider the top max_features ordered by term
        frequency across the corpus. Otherwise, all features are used.
    binary : bool, default=True
        If True, all non-zero term counts are set to 1. This does not mean outputs will have only
        0/1 values, only that the tf term in tf-idf is binary.
    norm : {'l1', 'l2'}, default='l2'
        Each output row will have unit norm, either: ‘l2’: Sum of squares of vector elements is 1.
        The cosine similarity between two vectors is their dot product when l2 norm has been
        applied. ‘l1’: Sum of absolute values of vector elements is 1. None: No normalization.
    use_idf : bool, default=False
        Enable inverse-document-frequency reweighting. If False, idf(t) = 1.
    smooth_idf : bool, default=True
        Smooth idf weights by adding one to document frequencies, as if an extra document was seen
        containing every term in the collection exactly once. Prevents zero divisions.
    sublinear_tf : bool, default=False
        Apply sublinear tf scaling, i.e. replace tf with 1 + log(tf).
    C : float, default=10.0
        Inverse of regularization strength for Logistic Regression. Smaller values
        specify stronger regularization.
    l1_ratio : float, default=0
        The Elastic Net mixing parameter, with 0 <= l1_ratio <= 1.
    stack_folds : int, default=5
        Number of folds for cross-validation in the stacking process.
    random_state : int, default=42
        Random state for reproducibility.

    Attributes
    ----------
    pipeline : sklearn.pipeline.Pipeline
        The underlying pipeline object which consists of the TF-IDF vectorizer
        and a stacking transformer wrapping a Logistic Regression classifier.

    Examples
    --------
    >>> import pandas as pd
    >>> import numpy as np
    >>> from sklearn.model_selection import train_test_split
    >>> from sklearn.metrics import accuracy_score
    >>> import base64

    # Sample DataFrame
    >>> data = {'text_column': ['sample text', 'another sample text', ...]}
    >>> df = pd.DataFrame(data)
    >>> y = np.array([0, 1, ...])  # Sample target array

    # Base64 encode the column name 'text_column'
    >>> encoded_column_name = base64.b64encode('text_column'.encode('utf-8')).decode('utf-8')

    # Initialize and use StackedNgramClassifier
    >>> model = StackedNgramClassifier(tfidf_column=encoded_column_name)
    >>> X_train, X_test, y_train, y_test = train_test_split(df, y, test_size=0.2, random_state=42)
    >>> model.fit(X_train, y_train)
    >>> y_pred = model.predict(X_test)
    >>> print(f"Accuracy: {accuracy_score(y_test, y_pred)}")
    """

    def __init__(
        self,
        lowercase: bool = True,
        analyzer: Union[str, Callable[..., Any]] = "word",
        max_ngram: int = 2,
        min_ngram: int = 1,
        max_df: Union[float, int] = 0.8,
        min_df: Union[float, int] = 1,
        max_features: Union[None, int] = 20000,
        binary: bool = True,
        norm: Union[str, int] = "l2",
        use_idf: bool = False,
        smooth_idf: bool = True,
        sublinear_tf: bool = False,
        C: float = 10.0,
        l1_ratio: float = 0,
        stack_folds: int = 5,
        random_state: int = 42,
    ) -> None:

        # Convert parameter types
        lowercase = bool(lowercase)
        binary = bool(binary)
        use_idf = bool(use_idf)
        smooth_idf = bool(smooth_idf)
        sublinear_tf = bool(sublinear_tf)

        if isinstance(norm, int):
            if norm in [1, 2]:
                norm = "l" + str(norm)
            else:
                raise ValueError("norm must be either 1 or 2 if it is an integer.")

        self.lowercase: bool = lowercase
        self.analyzer: Union[str, Callable[..., Any]] = analyzer
        self.max_ngram: int = max_ngram
        self.min_ngram: int = min_ngram
        self.max_df: Union[float, int] = max_df
        self.min_df: Union[float, int] = min_df
        self.max_features = max_features
        self.binary: bool = binary
        self.norm: str = norm
        self.use_idf: bool = use_idf
        self.smooth_idf: bool = smooth_idf
        self.sublinear_tf: bool = sublinear_tf
        self.C: float = C
        self.l1_ratio: float = l1_ratio
        self.stack_folds: int = stack_folds
        self.random_state: int = random_state

        tfidf: TfidfVectorizer = TfidfVectorizer(
            analyzer=self.analyzer,
            ngram_range=(self.min_ngram, self.max_ngram),
            max_df=self.max_df,
            min_df=self.min_df,
            max_features=self.max_features,
            binary=self.binary,
            norm=self.norm,
            use_idf=self.use_idf,
            smooth_idf=self.smooth_idf,
            sublinear_tf=self.sublinear_tf,
            lowercase=self.lowercase,
        )

        classifier: LogisticRegression = LogisticRegression(
            solver="saga",
            penalty="elasticnet",
            C=self.C,
            l1_ratio=self.l1_ratio,
            random_state=self.random_state,
        )

        # TfidfVectorizer can only handle one columnm, so we use the first column in the data only
        super().__init__(
            [
                ("tfidf", ColumnTransformer([("tfidf", tfidf, 0)])),
                (
                    "classifier",
                    StackingTransformer(
                        [("classifier", classifier)],
                        regression=False,
                        needs_proba=True,
                        n_folds=stack_folds,
                        shuffle=True,
                        variant="B",
                        stratified=True,
                        random_state=random_state,
                    ),
                ),
            ]
        )


class StackedNgramRegressor(Pipeline):  # type: ignore[misc]
    """
    A simple and compact text vectorizer. Selects a single text column (defined as a base64 encoded
    string) and tf-idf encodes it.

    Then fits a stacked ElasticNet regression on top of it.

    Useful with tree based models like Xgboost.

    [Rest of the docstring, update as needed for the regressor context]

    Parameters
    ----------
    lowercase : bool, default=True
        Convert all characters to lowercase before tokenizing.
    analyzer : {'word', 'char', 'char_wb'} or callable, default='word'
        Whether the feature should be made of word or character n-grams. Option ‘char_wb’ creates
        character n-grams only from text inside word boundaries; n-grams at the edges of words are
        padded with space. If a callable is passed it is used to extract the sequence of features
        out of the raw, unprocessed input.
    max_ngram : int, default=2
        The upper boundary of the range of n-values for different n-grams to be extracted. Only
        applies if analyzer is not callable.
    min_ngram : int, default=1
        The lower boundary of the range of n-values for different n-grams to be extracted. Only
        applies if analyzer is not callable.
    max_df : float or int, default=0.8
        When building the vocabulary ignore terms that have a document frequency strictly higher
        than the given threshold (corpus-specific stop words). If float in range [0.0, 1.0], the
        parameter represents a proportion of documents, integer absolute counts.
    min_df : float or int, default=2
        When building the vocabulary ignore terms that have a document frequency strictly lower than
        the given threshold. This value is also called cut-off in the literature. If float in range
        of [0.0, 1.0], the parameter represents a proportion of documents, integer absolute counts.
    max_features : int, default=20000
        If not None, build a vocabulary that only consider the top max_features ordered by term
        frequency across the corpus. Otherwise, all features are used.
    binary : bool, default=True
        If True, all non-zero term counts are set to 1. This does not mean outputs will have only
        0/1 values, only that the tf term in tf-idf is binary.
    norm : {'l1', 'l2'}, default='l2'
        Each output row will have unit norm, either: ‘l2’: Sum of squares of vector elements is 1.
        The cosine similarity between two vectors is their dot product when l2 norm has been
        applied. ‘l1’: Sum of absolute values of vector elements is 1. None: No normalization.
    use_idf : bool, default=False
        Enable inverse-document-frequency reweighting. If False, idf(t) = 1.
    smooth_idf : bool, default=True
        Smooth idf weights by adding one to document frequencies, as if an extra document was seen
        containing every term in the collection exactly once. Prevents zero divisions.
    sublinear_tf : bool, default=False
        Apply sublinear tf scaling, i.e. replace tf with 1 + log(tf).
    C : float, default=100.0
        Inverse of regularization strength for Logistic Regression. Smaller values
        specify stronger regularization.
    l1_ratio : float, default=0
        The Elastic Net mixing parameter, with 0 <= l1_ratio <= 1.
    stack_folds : int, default=5
        Number of folds for cross-validation in the stacking process.
    random_state : int, default=42
        Random state for reproducibility.

    Examples
    --------
    >>> import pandas as pd
    >>> import numpy as np
    >>> from sklearn.model_selection import train_test_split
    >>> from sklearn.metrics import mean_squared_error
    >>> import base64

    # Sample DataFrame
    >>> data = {'text_column': ['sample text', 'another sample text', 'more text', 'further text', 'additional text']}
    >>> df = pd.DataFrame(data)
    >>> y = np.array([1.5, 2.3, 0.7, 3.6, 2.1])  # Sample target values for regression

    # Base64 encode the column name 'text_column'
    >>> encoded_column_name = base64.b64encode('text_column'.encode('utf-8')).decode('utf-8')

    # Initialize and use StackedNgramRegressor
    >>> model = StackedNgramRegressor(tfidf_column=encoded_column_name)
    >>> X_train, X_test, y_train, y_test = train_test_split(df, y, test_size=0.2, random_state=42)
    >>> model.fit(X_train, y_train)
    >>> y_pred = model.predict(X_test)
    >>> print(f"Mean Squared Error: {mean_squared_error(y_test, y_pred)}")

    Attributes
    ----------
    pipeline : sklearn.pipeline.Pipeline
        The underlying pipeline object which consists of the TF-IDF vectorizer
        and a stacking transformer wrapping an ElasticNet regressor.
    """

    def __init__(
        self,
        lowercase: bool = True,
        analyzer: Union[str, Callable[..., Any]] = "word",
        max_ngram: int = 2,
        min_ngram: int = 1,
        max_df: Union[float, int] = 0.8,
        min_df: Union[float, int] = 1,
        max_features: Union[None, int] = 20000,
        binary: bool = True,
        norm: Union[str, int] = "l2",
        use_idf: bool = False,
        smooth_idf: bool = True,
        sublinear_tf: bool = False,
        C: float = 100.0,
        l1_ratio: float = 0,
        stack_folds: int = 5,
        random_state: int = 42,
    ) -> None:

        # Convert parameter types
        lowercase = bool(lowercase)
        binary = bool(binary)
        use_idf = bool(use_idf)
        smooth_idf = bool(smooth_idf)
        sublinear_tf = bool(sublinear_tf)

        if isinstance(norm, int):
            if norm in [1, 2]:
                norm = "l" + str(norm)
            else:
                raise ValueError("norm must be either 1 or 2 if it is an integer.")

        self.lowercase: bool = lowercase
        self.analyzer: Union[str, Callable[..., Any]] = analyzer
        self.max_ngram: int = max_ngram
        self.min_ngram: int = min_ngram
        self.max_df: Union[float, int] = max_df
        self.min_df: Union[float, int] = min_df
        self.max_features = max_features
        self.binary: bool = binary
        self.norm: str = norm
        self.use_idf: bool = use_idf
        self.smooth_idf: bool = smooth_idf
        self.sublinear_tf: bool = sublinear_tf
        self.C: float = C
        self.l1_ratio: float = l1_ratio
        self.stack_folds: int = stack_folds
        self.random_state: int = random_state

        tfidf = TfidfVectorizer(
            analyzer=self.analyzer,
            ngram_range=(self.min_ngram, self.max_ngram),
            max_df=self.max_df,
            min_df=self.min_df,
            max_features=self.max_features,
            binary=self.binary,
            norm=self.norm,
            use_idf=self.use_idf,
            smooth_idf=self.smooth_idf,
            sublinear_tf=self.sublinear_tf,
            lowercase=self.lowercase,
        )

        regressor = ElasticNet(
            alpha=1 / self.C, l1_ratio=self.l1_ratio, random_state=self.random_state
        )

        # TfidfVectorizer can only handle one columnm, so we use the first column in the data only
        super().__init__(
            [
                ("tfidf", ColumnTransformer([("tfidf", tfidf, 0)])),
                (
                    "regressor",
                    StackingTransformer(
                        [("regressor", regressor)],
                        regression=True,
                        needs_proba=False,
                        n_folds=self.stack_folds,
                        shuffle=True,
                        variant="B",
                        stratified=False,
                        random_state=self.random_state,
                    ),
                ),
            ]
        )

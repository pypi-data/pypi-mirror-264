import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.impute import SimpleImputer
from collections import defaultdict
from tabulate import tabulate


def read_file(file_path):
    """
    Read data from different file formats.

    Args:
        file_path (str): Path to the file.

    Returns:
        DataFrame: Loaded data.
    """
    if file_path.endswith(".csv"):
        return pd.read_csv(file_path)
    elif file_path.endswith(".xlsx") or file_path.endswith(".xls"):
        return pd.read_excel(file_path)
    elif file_path.endswith(".json"):
        return pd.read_json(file_path)
    else:
        raise ValueError("Unsupported file format")


def get_summary_statistics(data):
    """
    Calculate summary statistics of the data.

    Args:
        data (DataFrame): Input data.

    Returns:
        DataFrame: Summary statistics.
    """
    return data.describe()


def get_mode(data):
    """
    Calculate the mode of the data.

    Args:
        data (DataFrame): Input data.

    Returns:
        Series: Mode of the data.
    """
    return data.mode().iloc[0]


def get_average(data):
    """
    Calculate the average of the data.

    Args:
        data (DataFrame): Input data.

    Returns:
        Series: Average of the data.
    """
    return data.mean(numeric_only=True)


def get_summary(data):
    """
    Generate a summary of the data.

    Args:
        data (DataFrame): Input data.

    Returns:
        dict: Summary information.
    """
    summary = defaultdict(dict)
    summary["Summary Statistics"] = get_summary_statistics(data)
    summary["Mode"] = get_mode(data)
    summary["Average"] = get_average(data)
    return dict(summary)


def remove_missing_values(data):
    """
    Remove rows with missing values from the data.

    Args:
        data (DataFrame): Input data.

    Returns:
        DataFrame: Data with missing values removed.
    """
    return data.dropna()


def impute_missing_values(data, strategy="mean"):
    """
    Impute missing values in the data based on the specified strategy.

    Args:
        data (DataFrame): Input data.
        strategy (str): Imputation strategy ('mean', 'median', or 'most_frequent').

    Returns:
        DataFrame: Data with missing values imputed.
    """
    imputer = SimpleImputer(strategy=strategy)
    return pd.DataFrame(imputer.fit_transform(data), columns=data.columns)


def handle_missing_values(data, strategy="remove"):
    """
    Handle missing values in the data.

    Args:
        data (DataFrame): Input data.
        strategy (str): Missing value handling strategy ('remove' or imputation strategy).

    Returns:
        DataFrame: Data with missing values handled.
    """
    if strategy == "remove":
        return remove_missing_values(data)
    else:
        return impute_missing_values(data, strategy)


def one_hot_encode(data):
    """
    Perform one-hot encoding on categorical columns of the data.

    Args:
        data (DataFrame): Input data.

    Returns:
        DataFrame: Data with one-hot encoded columns.
    """
    if len(data) == 0:
        return data
    else:
        categorical_cols = data.select_dtypes(include=["object", "category"]).columns
        if len(categorical_cols) == 0:
            return data
        else:
            encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
            encoded_data = encoder.fit_transform(data[categorical_cols])
            encoded_df = pd.DataFrame(
                encoded_data, columns=encoder.get_feature_names_out(categorical_cols)
            )
            return pd.concat([data.drop(columns=categorical_cols), encoded_df], axis=1)


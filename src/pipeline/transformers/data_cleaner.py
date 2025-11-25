"""Data cleaning and validation."""

import pandas as pd
import numpy as np
from typing import List
from src.utils.logger import get_logger

logger = get_logger(__name__)


class DataCleaner:
    """Clean and validate data."""

    @staticmethod
    def remove_duplicates(df: pd.DataFrame, subset: List[str] = None) -> pd.DataFrame:
        """Remove duplicate rows."""
        initial_count = len(df)
        df_cleaned = df.drop_duplicates(subset=subset)
        removed = initial_count - len(df_cleaned)
        if removed > 0:
            logger.info(f"Removed {removed} duplicate rows")
        return df_cleaned

    @staticmethod
    def handle_missing_values(df: pd.DataFrame, strategy: str = "drop") -> pd.DataFrame:
        """Handle missing values."""
        missing_count = df.isnull().sum().sum()
        if missing_count == 0:
            return df

        logger.info(f"Found {missing_count} missing values")

        if strategy == "drop":
            df_cleaned = df.dropna()
            logger.info(f"Dropped rows with missing values")
        elif strategy == "fill_mean":
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            df_cleaned = df.copy()
            df_cleaned[numeric_cols] = df_cleaned[numeric_cols].fillna(
                df_cleaned[numeric_cols].mean()
            )
            logger.info(f"Filled missing numeric values with mean")
        elif strategy == "fill_zero":
            df_cleaned = df.fillna(0)
            logger.info(f"Filled missing values with 0")
        else:
            df_cleaned = df

        return df_cleaned

    @staticmethod
    def remove_outliers(
        df: pd.DataFrame, column: str, method: str = "iqr", threshold: float = 1.5
    ) -> pd.DataFrame:
        """Remove outliers from a numeric column."""
        if column not in df.columns or not pd.api.types.is_numeric_dtype(df[column]):
            return df

        initial_count = len(df)

        if method == "iqr":
            Q1 = df[column].quantile(0.25)
            Q3 = df[column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - threshold * IQR
            upper_bound = Q3 + threshold * IQR
            df_cleaned = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
        elif method == "zscore":
            z_scores = np.abs((df[column] - df[column].mean()) / df[column].std())
            df_cleaned = df[z_scores < threshold]
        else:
            df_cleaned = df

        removed = initial_count - len(df_cleaned)
        if removed > 0:
            logger.info(f"Removed {removed} outliers from {column}")

        return df_cleaned

    @staticmethod
    def validate_date_range(df: pd.DataFrame, date_column: str, start_date, end_date) -> pd.DataFrame:
        """Validate dates are within expected range."""
        if date_column not in df.columns:
            return df

        df[date_column] = pd.to_datetime(df[date_column])
        initial_count = len(df)
        df_valid = df[(df[date_column] >= start_date) & (df[date_column] <= end_date)]
        removed = initial_count - len(df_valid)

        if removed > 0:
            logger.info(f"Removed {removed} rows with dates outside range")

        return df_valid

    @staticmethod
    def validate_positive_values(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        """Ensure specified columns have positive values."""
        df_valid = df.copy()
        for col in columns:
            if col in df_valid.columns and pd.api.types.is_numeric_dtype(df_valid[col]):
                initial_count = len(df_valid)
                df_valid = df_valid[df_valid[col] > 0]
                removed = initial_count - len(df_valid)
                if removed > 0:
                    logger.info(f"Removed {removed} rows with non-positive {col}")

        return df_valid

